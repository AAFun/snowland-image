# -*- coding: utf-8 -*-
import numpy as np

from snowland.gis_tool.transformer import utm_transformer, gps_transformer
import random
from astartool.project import time_clock

npa = np.array

n = 10000

lat = [random.random() * 354 - 177 for i in range(n)]
lon = [random.random() * 354 - 177 for i in range(n)]

start = time_clock()
ux1, uy1 = utm_transformer(lat, lon)
zone_number = (npa(lon) / 6).astype(int) + 31

print(ux1, uy1)
end1 = time_clock()

# end2 = time_clock()
# utm = [utm_transformer(la, lo) for (la, lo) in zip(lat, lon)]
# end3 = time_clock()

print("time1:", end1 - start)
# print("time2:", end3 - end2)
# assert utm == [(a, b)for a, b in zip(ux1, uy1)]

lat_new, lon_new = gps_transformer(ux1, uy1, zone_number)
print(ux1, uy1)
print(lat[:15])
print(lat_new[:15])
assert np.all(np.isclose(lat, lat_new))
assert np.all(np.isclose(lon, lon_new))
