import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import contextily as ctx
import pandas as pd
import networkx as nx
from shapely.geometry import box, LineString
import matplotlib.patches as mpatches

# Define file path (Update this if needed)
file_path = r"C:\Users\Lydiah\PyCharmProjects\PythonProject\PythonProject\UrbanPlanning_NRB\data\nairobi_roads\nairobi_roads_2010.shp"  # Ensure the path is correct

# Load Nairobi Roads dataset
nairobi_roads = gpd.read_file(file_path)

# Display dataset info
print(f"Total Roads: {len(nairobi_roads)}")
print("Columns:", nairobi_roads.columns.tolist())

# Identify High & Low Road Density Areas
grid_size = 5000  # Grid size in meters
xmin, ymin, xmax, ymax = nairobi_roads.total_bounds  # Get dataset bounds

x_coords = np.arange(xmin, xmax, grid_size)
y_coords = np.arange(ymin, ymax, grid_size)
grid_cells = [gpd.GeoDataFrame(geometry=[box(x, y, x + grid_size, y + grid_size)], crs=nairobi_roads.crs)
              for x in x_coords for y in y_coords]
grid = gpd.GeoDataFrame(pd.concat(grid_cells, ignore_index=True))

grid["road_count"] = grid.geometry.apply(lambda cell: nairobi_roads[nairobi_roads.intersects(cell)].shape[0])

# Define thresholds for high & low density
high_density_threshold = grid["road_count"].quantile(0.75)
low_density_threshold = grid["road_count"].quantile(0.25)

high_density = grid[grid["road_count"] >= high_density_threshold]
low_density = grid[grid["road_count"] <= low_density_threshold]

#Plot High & Low-Density Roads (Fixed Legends)
fig, ax = plt.subplots(figsize=(12, 12))
grid.plot(ax=ax, column="road_count", cmap="OrRd", legend=True, alpha=0.7)
high_density.plot(ax=ax, color="red", alpha=0.5)
low_density.plot(ax=ax, color="blue", alpha=0.5)
nairobi_roads.plot(ax=ax, color="black", linewidth=0.3, alpha=0.5)

# Manually Add Legend
high_density_patch = mpatches.Patch(color="red", alpha=0.5, label="High-Density Roads")
low_density_patch = mpatches.Patch(color="blue", alpha=0.5, label="Low-Density Areas")
plt.legend(handles=[high_density_patch, low_density_patch])

plt.title("Nairobi Road Density: High vs Low Connectivity")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

#Shortest Path Analysis (Fixed LineString Error)
G = nx.Graph()

for _, road in nairobi_roads.iterrows():
    coords = list(road.geometry.coords)
    for i in range(len(coords) - 1):
        G.add_edge(coords[i], coords[i + 1], weight=road["Shape_Leng"])

start = list(G.nodes())[0]
end = list(G.nodes())[-1]

shortest_path = nx.shortest_path(G, source=start, target=end, weight="weight")

# Convert to GeoDataFrame (FIXED: Use Shapely LineString)
path_geometry = gpd.GeoSeries([LineString(shortest_path)], crs=nairobi_roads.crs)

# Plot Shortest Path
fig, ax = plt.subplots(figsize=(12, 12))
nairobi_roads.plot(ax=ax, color="gray", linewidth=0.3, alpha=0.5, label="Road Network")
path_geometry.plot(ax=ax, color="red", linewidth=2, label="Shortest Path")

plt.legend()
plt.title("Shortest Path in Nairobi's Road Network")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()