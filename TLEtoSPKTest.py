import numpy as np
from plotly.offline import init_notebook_mode, plot
from plotly.graph_objs import Scatter3d, Line, Data, Layout
import spiceypy as spice
init_notebook_mode()

spice.furnsh("kernels/ISS/ISS.bsp")
spice.furnsh("kernels/ASU_gs/ASUGS.bsp")
#spice.furnsh("kernels/pck/cpck05Mar2004.tpc")
#spice.furnsh("kernels/leap_seconds/naif0007.tls")
spice.furnsh("kernels/leap_seconds/naif0011.tls")
spice.furnsh("kernels/pck/pck00010.tpc")

step = 20000

# Get et values one and two, we could vectorize str2et
etOne = spice.str2et('Jun 11, 2017')
etTwo = spice.str2et('Jun 14, 2017')

# get times
times = np.linspace(etOne, etTwo, step, endpoint=False)

# Run spkpos as a vectorized function
positions, lightTimes = spice.spkpos('-125544', times, 'IAU_EARTH', 'NONE', '-999999')

# Positions is a 3xN vector of XYZ positions
print("Positions: ")
print(positions[0])

# Light times is a N vector of time
print("Light Times: ")
print(lightTimes[0])

# Clean up the kernels
spice.kclear()

threeDPlot = Scatter3d(
    x=positions[:, 0],  # X coordinates
    y=positions[:, 1],  # Y coordinates
    z=positions[:, 2],  # Z coordinates
    name='MinXSS',
    mode='lines',
    line=Line(width=3)
)

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

data = Data([threeDPlot, barycenter])

layout = Layout(title="ISS TLE->SPK MKSPK demonstration")

fig = dict(data=data, layout=layout)
#plot(fig)
print (etOne)
print (etTwo)

