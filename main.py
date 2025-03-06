import matplotlib.pyplot as plt
import geopandas as gpd
import fiona

# Load the Nairobi roads dataset
file_path  = r"C:\Users\Lydiah\PyCharmProjects\PythonProject\PythonProject\UrbanPlanning_NRB\data\nairobi_roads\nairobi_roads_2010.shp"
nairobi_roads = gpd.read_file(file_path)

# Display dataset info
print("📊 Dataset Overview:")
print(f"Total Roads: {len(nairobi_roads)}")
print("Columns:", nairobi_roads.columns.tolist())
print("Coordinate Reference System (CRS):", nairobi_roads.crs)
print(nairobi_roads.head())  # Preview first few records

# 🚀 Plot Full Nairobi Road Network
fig, ax = plt.subplots(figsize=(12, 12))
nairobi_roads.plot(ax=ax, color="blue", linewidth=0.5)

plt.title("Nairobi Road Network (2010)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

# 🚀 Highlight Major Roads (Highways, Expressways)
major_roads = nairobi_roads[nairobi_roads["NAME"].str.contains("HIGHWAY|EXPRESSWAY|ROAD", na=False, case=False)]

# Plot major roads in red
fig, ax = plt.subplots(figsize=(12, 12))
nairobi_roads.plot(ax=ax, color="blue", linewidth=0.3, alpha=0.5)
major_roads.plot(ax=ax, color="red", linewidth=1)

plt.title("Major Roads in Nairobi (2010)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

