import numpy as np
from plotly.offline import init_notebook_mode, plot
from plotly.graph_objs import Scatter3d, Line, Data, Layout
import spiceypy as spice
import math
import spacetrack
import csv
init_notebook_mode()


spice.furnsh("kernels/ISS/ISS.bsp")
spice.furnsh("kernels/CityImages.bsp")
spice.furnsh("kernels/leap_seconds/naif0011.tls")
spice.furnsh("kernels/pck/pck00010.tpc")
spice.furnsh("kernels/geophysical.ker")
spice.furnsh("kernels/CityImages.tf")

step =100000

satellite_norad = 25544
satellite_naif_id = str(-100000 - satellite_norad)
gs_naif_id = "-9999999"
cover = spice.utils.support_types.SPICEDOUBLE_CELL(200000)

spice.spkcov("kernels/ISS/ISS.bsp", int(satellite_naif_id), cover)
coverWIN = spice.wnfetd(cover,0)
etStart = coverWIN[0]
etStop = coverWIN[1]


# get times
times = np.linspace(etStart, etStop, step, endpoint=False)

# Run spkpos as a vectorized function
positions, lightTimes = spice.spkpos('-125544', times, 'IAU_EARTH', 'NONE', 'EARTH')

# Clean up the kernels

#spice.kclear()

utc = [etStart, etStop]

TIMFMT = "YYYY MON DD HR:MN:SC.###### TDB::RND::TDB"

target   = "-125544"
obsrvr   = "-1111111"
inframe  = "ASU-GS_TOPO"
crdsys   = "LATITUDINAL"
coord    = "LATITUDE"
relate   = ">"
refval   = math.radians(5)
step     = 30
nintvals = 100000
adjust   = 0.0
abcorr   = "NONE"
cnfine   = spice.stypes.SPICEDOUBLE_CELL(200000)
result   = spice.stypes.SPICEDOUBLE_CELL(200000)

spice.wninsd(*utc, cnfine)

spice.gfposc(target, inframe, abcorr, obsrvr, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine, result)

spice.wnfetd(result, 0)

# get times
times = []
for i in range(spice.wncard(result)):
    times.append(np.linspace(*spice.wnfetd(result, i), step, endpoint=False))

for time in times:
    t = spice.timout(time, TIMFMT)
    #t = spice.et2utc(time, 'C', 14)
    s = time[0]
    st = time[-1]
    duration = (st -s)
    start = t[0]
    stop  = t[-1]
    closest_approach = spice.timout((st+s)/2, TIMFMT)
    print("Start: {}   Stop: {} Closest Approach: {}".format(start, stop, closest_approach))

positions1 = []
for i, _ in enumerate(times):
    positions1.append(spice.spkpos('-125544', times[i], 'IAU_EARTH', 'NONE', 'EARTH')[0])

positionsearth=[]
for i, _ in enumerate(times):
    positionsearth.append(spice.spkpos('-125544', times[i], 'IAU_EARTH', 'NONE', 'EARTH')[0])

#print(positions1)
threeDPlot = Scatter3d(
    x=positions[:, 0],  # X coordinates
    y=positions[:, 1],  # Y coordinates
    z=positions[:, 2],  # Z coordinates
    name='MinXSS',
    mode='lines',
    line=Line(width=3)
)

threeDPlot1 = []
for i, _ in enumerate(positions1):
    threeDPlot1.append(Scatter3d(
        x=positions1[i][:, 0],  # X coordinates
        y=positions1[i][:, 1],  # Y coordinates
        z=positions1[i][:, 2],  # Z coordinates
        name='MinXSS',
        mode='lines',
        line=Line(width=10,
                  color='red')
    ))

barycenter = Scatter3d(
    x=[0],
    y=[0],
    z=[0],
    name='bc',
    mode='marker',
    marker=dict(
        size=5,
        color='orange'
    )
)

data = Data([threeDPlot, *threeDPlot1, barycenter])

layout = Layout(title="ISS TLE->SPK MKSPK demonstration")

fig = dict(data=data, layout=layout)
#plot(fig)

# Get et values one and two, we could vectorize str2et
#etStarttemp = spice.str2et('2017 Sep 13, 12:00:00 TDB')
#etStoptemp = spice.str2et('2017 Sep 13, 16:00:00 TDB')

#utctemp= [etStarttemp, etStoptemp]

# get times
#timestemp = np.linspace(etStarttemp, etStoptemp, 10000, endpoint=False)

# Run spkpos as a vectorized function
#positionstemp, lightTimestemp = spice.spkpos('-125544', timestemp, 'IAU_EARTH', 'NONE', 'EARTH')

# temparray = np.asarray(positionstemp)

#result   = spice.stypes.SPICEDOUBLE_CELL(200000)

#Latlongpositionstemp=[]
#for objecttemp in positionstemp:
#    coordtemp = list(spice.reclat(objecttemp))
#    coordtemp[1:] = map(math.degrees, coordtemp[1:])
#    Latlongpositionstemp.append(coordtemp[1:])
#for object in timestemp:
#    Latlongpositionstemp.append(str(object[0]))


#merged = np.column_stack((timestemp, Latlongpositionstemp))
#print(merged)

Latlongpositions=[]
for object in positionsearth:
    for coord in object:
        #print("Before: {}".format(coord))
        coord = list(spice.reclat(coord))
        coord[1:] = map(math.degrees, coord[1:])
        #print("After:  {}".format
        Latlongpositions.append(str(coord[1:]))

#with open('Groundtrackstest4.csv', "w") as output:
#    writer = csv.writer(output, lineterminator='\n')
#    for latlong in merged:
#        writer.writerows(merged)

#with open("GT.csv", "w") as f:
#        writer = csv.writer(f)
#        writer.writerows(merged)

#print("\n".join(Latlongpositions))


