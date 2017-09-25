import spiceypy as spice
import math

spice.furnsh("kernels/ISS/ISS.bsp")
spice.furnsh("kernels/ASU_gs/ASUGS.bsp")
spice.furnsh("kernels/leap_seconds/naif0011.tls")
spice.furnsh("kernels/pck/pck00010.tpc")

# we are going to get positions between these two dates
utc = [spice.str2et('Jun 11, 2017'), spice.str2et('Jun 14, 2017')]

TIMFMT = "YYYY MON DD HR:MN:SC.###### TDB::RND::TDB"

target   = "-125544"
obsrvr   = "-999999"
inframe  = "IAU_EARTH"
crdsys   = "LATITUDINAL"
coord    = "LATITUDE"
relate   = ">"
refval   = math.radians(65)
step     = 30
nintvals = 100000
adjust   = 0.0
abcorr   = "NONE"
cnfine   = spice.stypes.SPICEDOUBLE_CELL(200000)
result   = spice.stypes.SPICEDOUBLE_CELL(200000)

spice.wninsd(*utc, cnfine)

spice.gfposc(target, inframe, abcorr, obsrvr, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine, result)

print(result)

for i in range(spice.wncard(result)):
    k = spice.wnfetd(result, i)
    print("{}    {}".format(spice.timout(k[0], TIMFMT), spice.timout(k[1], TIMFMT)))

for i in range(spice.wncard(result)):
    x = spice.wnfetd(result, i)
    print(x)