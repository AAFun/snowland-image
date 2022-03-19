

EARTH_RADIUS = 6378.137  # 初始化地球半径km

RULE_MORTON = (1 << 32) / 360.0
RULE_MORTON_TO_LONLAT = 360.0 / (1 << 32)
NDS_90_DEGREES = 0x3fffffff
NDS_180_DEGREES = 0x7fffffff
NDS_360_DEGREES = 4294967295


from snowland.gis_tool import gis_helper, haversine, nds, transformer
