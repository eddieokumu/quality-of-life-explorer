import geopandas as gpd

print("Reading from zip...")
gdf = gpd.read_file("zip://data/shapefiles/gadm40_KEN_3.zip!gadm40_KEN_3.shp")
print(f"Total features: {len(gdf)}")

