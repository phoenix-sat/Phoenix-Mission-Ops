# CITY = (lat, long, alt) PAY ATTENTION TO ORDER
CHICAGO      = (- 87.6298, 41.8781, 181)
PHOENIX      = (-112.0740, 33.4484, 331)
LOS_ANGELES  = (-118.2437, 34.0522,  71)
HOUSTON      = (- 95.3698, 29.7604,  24)
MINNEAPOLIS  = (- 93.2650, 44.9778, 253)
BALTIMORE    = (- 76.6122, 39.2904, 150)
ATLANTA      = (- 84.3880, 33.7490, 320)

if __name__ == "cities":

    import spiceypy as spice
    import math

    RE = 6378137
    F = 1 / 298.257223563

    print(spice.georec(math.radians(CHICAGO[0]), math.radians(CHICAGO[1]), CHICAGO[2], RE, F))

