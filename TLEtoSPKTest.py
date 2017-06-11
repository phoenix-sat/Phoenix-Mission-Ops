import numpy as np
from plotly.offline import init_notebook_mode, plot
from plotly.graph_objs import Scatter3d, Line, Data, Layout
import spiceypy as spice
init_notebook_mode()

spice.furnsh("minXSS.bsp")
spice.furnsh("cpck05Mar2004.tpc")
spice.furnsh("naif0007.tls")

step = 2000

# Get et values one and two, we could vectorize str2et
etOne = spice.str2et('Jun 20, 2016')
etTwo = spice.str2et('Jun 21, 2016')

# get times
times = np.linspace(etOne, etTwo, step, endpoint=False)

# Run spkpos as a vectorized function
positions, lightTimes = spice.spkpos('41474', times, 'J2000', 'NONE', 'EARTH')

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
        size=10,
        color='orange'
    )
)

data = Data([threeDPlot, barycenter])

layout = Layout(title="MinXSS TLE->SPK MKSPK demonstration")

fig = dict(data=data, layout=layout)
plot(fig)
