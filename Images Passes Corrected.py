import numpy as np
from plotly.offline import init_notebook_mode, plot
from plotly.graph_objs import Scatter3d, Line, Data, Layout
import spiceypy as spice
import math

init_notebook_mode()

spice.furnsh("kernels/ISS/ISS.bsp")
spice.furnsh("kernels/CityImages.bsp")
spice.furnsh("kernels/leap_seconds/naif0011.tls")
spice.furnsh("kernels/pck/pck00010.tpc")
spice.furnsh("kernels/geophysical.ker")
spice.furnsh("kernels/CityImages.tf")

#Define NAIF ID's
satellite_norad = 25544
satellite_naif_id = str(-100000 - satellite_norad)
gs_naif_id = "-9999999"
LA_naif_id = "-1111111"
CH_naif_id = "-2222222"
HO_naif_id = "-3333333"
BA_naif_id = "-4444444"
AT_naif_id = "-5555555"
MI_naif_id = "-6666666"

#Define Reference Frames
GS_frame = "ASU-GS_TOPO"
LA_frame = "LA-00_TOPO"
CH_frame = "CH-00_TOPO"
HO_frame = "HO-00_TOPO"
BA_frame = "BA-00_TOPO"
AT_frame = "AT-00_TOPO"
MI_frame = "MI-00_TOPO"


# Calculates window of time TLE will populate
cover = spice.utils.support_types.SPICEDOUBLE_CELL(200000)
spice.spkcov("kernels/ISS/ISS.bsp", int(satellite_naif_id), cover)
coverWIN = spice.wnfetd(cover,0)
etStart = coverWIN[0]
etStop = coverWIN[1]

# Retrieves times covered by TLE
step = 100000
times = np.linspace(etStart, etStop, step, endpoint=False)

# Run spkpos as a vectorized function
positions, lightTimes = spice.spkpos('-125544', times, 'IAU_EARTH', 'NONE', 'EARTH')

#Start and stop times covered by TLE
utc = [etStart, etStop]

#Creates a series of spice double cells
LA_result = spice.stypes.SPICEDOUBLE_CELL(200000)
CH_result = spice.stypes.SPICEDOUBLE_CELL(200000)
HO_result = spice.stypes.SPICEDOUBLE_CELL(200000)
BA_result = spice.stypes.SPICEDOUBLE_CELL(200000)
AT_result = spice.stypes.SPICEDOUBLE_CELL(200000)
MI_result = spice.stypes.SPICEDOUBLE_CELL(200000)
GS_result   = spice.stypes.SPICEDOUBLE_CELL(200000)
GS_trans_result = spice.stypes.SPICEDOUBLE_CELL(200000)


target   = "-125544"
obsrvr   = "-9999999"
inframe  = "ASU-GS_TOPO"
crdsys   = "LATITUDINAL"
coord    = "LATITUDE"
relate   = ">"
refval   = math.radians(65)
step     = 30
nintvals = 100000
adjust   = 0.0
abcorr   = "NONE"
cnfine   = spice.stypes.SPICEDOUBLE_CELL(200000)
transmission_refval = math.radians(10)

spice.wninsd(*utc, cnfine)

spice.gfposc(target, inframe, abcorr, obsrvr, crdsys, coord, relate, transmission_refval, adjust, step, nintvals, cnfine, GS_trans_result)
spice.wnfetd(GS_trans_result, 0)

spice.gfposc(target, inframe, abcorr, obsrvr, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine, GS_result)
spice.wnfetd(GS_result, 0)

spice.gfposc(target, "LA-00_TOPO", abcorr, LA_naif_id, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine, LA_result)
spice.wnfetd(LA_result, 0)

spice.gfposc(target, "CH-00_TOPO", abcorr, CH_naif_id, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine, CH_result)
spice.wnfetd(CH_result, 0)

spice.gfposc(target, "HO-00_TOPO", abcorr, HO_naif_id, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine, HO_result)
spice.wnfetd(HO_result, 0)

spice.gfposc(target, "BA-00_TOPO", abcorr, BA_naif_id, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine, BA_result)
spice.wnfetd(BA_result, 0)

spice.gfposc(target, "AT-00_TOPO", abcorr, AT_naif_id, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine, AT_result)
spice.wnfetd(AT_result, 0)

spice.gfposc(target, "MI-00_TOPO", abcorr, MI_naif_id, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine, MI_result)
spice.wnfetd(MI_result, 0)


#Creates an array of times in which it passes over target
GS_times = []
LA_times = []
CH_times = []
HO_times = []
BA_times = []
AT_times = []
MI_times = []
GS_trans_times =[]
The_times = [GS_times,LA_times,CH_times,HO_times,BA_times,AT_times,MI_times, GS_trans_times]
The_results = [GS_result,LA_result,CH_result,HO_result,BA_result,AT_result,MI_result, GS_trans_result]

for i in range(len(The_times)):
    for ii in range(spice.wncard(The_results[i])):
        The_times[i].append(np.linspace(*spice.wnfetd(The_results[i], ii), step, endpoint=False))


#for i in range(spice.wncard(LA_result)):
#   LA_times.append(np.linspace(*spice.wnfetd(LA_result, i), step, endpoint=False))

#for i in range(spice.wncard(CH_result)):
#    CH_times.append(np.linspace(*spice.wnfetd(CH_result, i), step, endpoint=False))

#for i in range(spice.wncard(HO_result)):
#    HO_times.append(np.linspace(*spice.wnfetd(HO_result, i), step, endpoint=False))

#for i in range(spice.wncard(BA_result)):
#    BA_times.append(np.linspace(*spice.wnfetd(BA_result, i), step, endpoint=False))

#for i in range(spice.wncard(AT_result)):
#    AT_times.append(np.linspace(*spice.wnfetd(AT_result, i), step, endpoint=False))

#for i in range(spice.wncard(MI_result)):
#    MI_times.append(np.linspace(*spice.wnfetd(MI_result, i), step, endpoint=False))

#Displaying Access Times
print("ASU Access Times:")
for GS_time in GS_times:
    Entrytime = spice.et2utc(GS_time[0], 'C', 4)
    Exittime = spice.et2utc(GS_time[-1], 'C', 4)
    closest_time = spice.et2utc((GS_time[0]+GS_time[-1])/2, 'C', 4)
    Duration = GS_time[-1]-GS_time[0]
    print("Start: {} Stop: {} Duration: {} Closest Approach: {}".format(Entrytime, Exittime, Duration, closest_time))

print("Los Angeles Access Times:")
for LA_time in LA_times:
    Entrytime = spice.et2utc(LA_time[0], 'C', 4)
    Exittime = spice.et2utc(LA_time[-1], 'C', 4)
    closest_time = spice.et2utc((LA_time[0]+LA_time[-1])/2, 'C', 4)
    print("Start: {}   Stop: {} Closest Approach: {}".format(Entrytime, Exittime, closest_time))

print("Chicago Access Times:")
for CH_time in CH_times:
    Entrytime = spice.et2utc(CH_time[0], 'C', 4)
    Exittime = spice.et2utc(CH_time[-1], 'C', 4)
    closest_time = spice.et2utc((CH_time[0]+CH_time[-1])/2, 'C', 4)
    print("Start: {}   Stop: {} Closest Approach: {}".format(Entrytime, Exittime, closest_time))

print("Houston Access Times:")
for HO_time in HO_times:
    Entrytime = spice.et2utc(HO_time[0], 'C', 4)
    Exittime = spice.et2utc(HO_time[-1], 'C', 4)
    closest_time = spice.et2utc((HO_time[0]+HO_time[-1])/2, 'C', 4)
    print("Start: {}   Stop: {} Closest Approach: {}".format(Entrytime, Exittime, closest_time))

print("Baltimore Access Times:")
for BA_time in BA_times:
    Entrytime = spice.et2utc(BA_time[0], 'C', 4)
    Exittime = spice.et2utc(BA_time[-1], 'C', 4)
    closest_time = spice.et2utc((BA_time[0]+BA_time[-1])/2, 'C', 4)
    print("Start: {}   Stop: {} Closest Approach: {}".format(Entrytime, Exittime, closest_time))

print("Atlanta Access Times:")
for AT_time in AT_times:
    Entrytime = spice.et2utc(AT_time[0], 'C', 4)
    Exittime = spice.et2utc(AT_time[-1], 'C', 4)
    closest_time = spice.et2utc((AT_time[0] + AT_time[-1]) / 2, 'C', 4)
    print("Start: {}   Stop: {} Closest Approach: {}".format(Entrytime, Exittime, closest_time))

print("Minneapolis Access Times:")
for MI_time in MI_times:
    Entrytime = spice.et2utc(MI_time[0], 'C', 4)
    Exittime = spice.et2utc(MI_time[-1], 'C', 4)
    closest_time = spice.et2utc((MI_time[0]+MI_time[-1])/2, 'C', 4)
    print("Start: {}   Stop: {} Closest Approach: {}".format(Entrytime, Exittime, closest_time))

print("GS Transmission Times:")
for GS_trans_time in GS_trans_times:
    Entrytime = spice.et2utc(GS_trans_time[0], 'C', 4)
    Exittime = spice.et2utc(GS_trans_time[-1], 'C', 4)
    closest_time = spice.et2utc((GS_trans_time[0]+GS_trans_time[-1])/2, 'C', 4)
    print("Start: {}   Stop: {} Closest Approach: {}".format(Entrytime, Exittime, closest_time))

#Calculating Positions Based on Access Times
positions_ASU=[]
for i, _ in enumerate(GS_times):
    positions_ASU.append(spice.spkpos('-125544', GS_times[i], 'IAU_EARTH', 'NONE', 'EARTH')[0])
positions_LA=[]
for i, _ in enumerate(LA_times):
    positions_LA.append(spice.spkpos('-125544', LA_times[i], 'IAU_EARTH', 'NONE', 'EARTH')[0])
positions_CH=[]
for i, _ in enumerate(CH_times):
    positions_CH.append(spice.spkpos('-125544', CH_times[i], 'IAU_EARTH', 'NONE', 'EARTH')[0])
positions_HO=[]
for i, _ in enumerate(HO_times):
    positions_HO.append(spice.spkpos('-125544', HO_times[i], 'IAU_EARTH', 'NONE', 'EARTH')[0])
positions_BA=[]
for i, _ in enumerate(BA_times):
    positions_BA.append(spice.spkpos('-125544', BA_times[i], 'IAU_EARTH', 'NONE', 'EARTH')[0])
positions_AT=[]
for i, _ in enumerate(AT_times):
    positions_AT.append(spice.spkpos('-125544', AT_times[i], 'IAU_EARTH', 'NONE', 'EARTH')[0])
positions_MI=[]
for i, _ in enumerate(MI_times):
    positions_MI.append(spice.spkpos('-125544', MI_times[i], 'IAU_EARTH', 'NONE', 'EARTH')[0])
positions_GS_trans=[]
for i, _ in enumerate(GS_trans_times):
    positions_GS_trans.append(spice.spkpos('-125544', GS_trans_times[i], 'IAU_EARTH', 'NONE', 'EARTH')[0])

#Calculate Optimal 3 Transmission Passes
print("Optimal 3 GS Transmission Passes:")
Transmission_Durations =[]
for GS_trans_time in GS_trans_times:
    Duration = GS_trans_time[-1] - GS_trans_time[0]
    Transmission_Durations.append(Duration)
for GS_trans_time in GS_trans_times:
    for i in range(0,3):
        if (sorted(Transmission_Durations, key=float, reverse=True)[i]) == (GS_trans_time[-1] - GS_trans_time[0]):
            Entrytime = spice.et2utc(GS_trans_time[0], 'C', 4)
            Exittime = spice.et2utc(GS_trans_time[-1], 'C', 4)
            print("Start: {}   Stop: {} Duration: {} seconds".format(Entrytime, Exittime, sorted(Transmission_Durations, key=float, reverse=True)[i]))

#Plotting
threeDPlot = Scatter3d(
    x=positions[:, 0],  # X coordinates
    y=positions[:, 1],  # Y coordinates
    z=positions[:, 2],  # Z coordinates
    name='ISS',
    mode='lines',
    line=Line(width=3)
)

threeDPlot_ASU = []
for i, _ in enumerate(positions_ASU):
    threeDPlot_ASU.append(Scatter3d(
        x=positions_ASU[i][:, 0],  # X coordinates
        y=positions_ASU[i][:, 1],  # Y coordinates
        z=positions_ASU[i][:, 2],  # Z coordinates
        name='ASU',
        mode='lines',
        line=Line(width=10,
                  color='red')
    ))

threeDPlot_LA = []
for i, _ in enumerate(positions_LA):
    threeDPlot_LA.append(Scatter3d(
        x=positions_LA[i][:, 0],  # X coordinates
        y=positions_LA[i][:, 1],  # Y coordinates
        z=positions_LA[i][:, 2],  # Z coordinates
        name='LA',
        mode='lines',
        line=Line(width=10,
                  color='red')
    ))

threeDPlot_CH = []
for i, _ in enumerate(positions_CH):
    threeDPlot_CH.append(Scatter3d(
        x=positions_CH[i][:, 0],  # X coordinates
        y=positions_CH[i][:, 1],  # Y coordinates
        z=positions_CH[i][:, 2],  # Z coordinates
        name='Chicago',
        mode='lines',
        line=Line(width=10,
                  color='red')
    ))

threeDPlot_HO = []
for i, _ in enumerate(positions_HO):
    threeDPlot_HO.append(Scatter3d(
        x=positions_HO[i][:, 0],  # X coordinates
        y=positions_HO[i][:, 1],  # Y coordinates
        z=positions_HO[i][:, 2],  # Z coordinates
        name='Houston',
        mode='lines',
        line=Line(width=10,
                  color='red')
    ))

threeDPlot_BA = []
for i, _ in enumerate(positions_BA):
    threeDPlot_BA.append(Scatter3d(
        x=positions_BA[i][:, 0],  # X coordinates
        y=positions_BA[i][:, 1],  # Y coordinates
        z=positions_BA[i][:, 2],  # Z coordinates
        name='Baltimore',
        mode='lines',
        line=Line(width=10,
                  color='red')
    ))

threeDPlot_AT = []
for i, _ in enumerate(positions_AT):
    threeDPlot_AT.append(Scatter3d(
        x=positions_AT[i][:, 0],  # X coordinates
        y=positions_AT[i][:, 1],  # Y coordinates
        z=positions_AT[i][:, 2],  # Z coordinates
        name='Atlanta',
        mode='lines',
        line=Line(width=10,
                  color='red')
    ))

threeDPlot_MI = []
for i, _ in enumerate(positions_MI):
    threeDPlot_MI.append(Scatter3d(
        x=positions_MI[i][:, 0],  # X coordinates
        y=positions_MI[i][:, 1],  # Y coordinates
        z=positions_MI[i][:, 2],  # Z coordinates
        name='Minneapolis',
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

data = Data([threeDPlot, *threeDPlot_ASU, *threeDPlot_LA, *threeDPlot_CH, *threeDPlot_HO, *threeDPlot_BA, *threeDPlot_AT, *threeDPlot_MI, barycenter])

layout = Layout(title="ISS TLE->SPK MKSPK demonstration")

fig = dict(data=data, layout=layout)
#plot(fig)
