# -*- coding: utf-8 -*-


from snowland.gis_tool.transformer import utm_transformer
import random
from astartool.project import time_clock

n = 10000

lat = [random.random() * 354 - 177 for i in range(n)]
lon = [random.random() * 354 - 177 for i in range(n)]

start = time_clock()
ux1, uy1 = utm_transformer(lat, lon)
print(ux1, uy1)
end1 = time_clock()

end2 = time_clock()
utm = [utm_transformer(la, lo) for (la, lo) in zip(lat, lon)]
end3 = time_clock()

print("time1:", end1 - start)
print("time2:", end3 - end2)
assert utm == [(a, b)for a, b in zip(ux1, uy1)]
