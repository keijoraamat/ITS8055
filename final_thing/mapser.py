import pandas as pd
import folium
import os

filepath ='sensor_positions.csv'
markers_url = "https://github.com/keijoraamat/ITS8055/blob/main/final_thing/img/{}".format
yellow_marker = "kollane_marker.png"
red_marker = "punane_marker.png"
green_marker = "roheline_marker.png"

data_dir = "data"

entries_in_ddir = os.listdir(data_dir)
dir_in_data = [entry for entry in entries_in_ddir if os.path.isdir(os.path.join(data_dir, entry))]

regions = []
region_sensors = {}
for dir in dir_in_data:

    # get region names
    region_name = dir[0:8]
    regions.append(region_name)
    sensors = []

    # get sensor names in region
    region_sensors_names = os.listdir(os.path.join(data_dir, dir))
    for name in region_sensors_names:
        name = name.split('-')[0]
        sensors.append(name)

    # add sensor names to region
    region_sensors[region_name] = sensors

# get sonsors coordinates
dfa = pd.read_csv(filepath, header=None)

dfa.columns = ['coords', 'name']

for i, row in dfa.iterrows():

    # add region name to matching senor
    for region, sensors in region_sensors.items():
        if dfa.loc[i, 'name'] in sensors:
            dfa.loc[i, 'region'] = region
    
    # parse coordinates
    coords = dfa.loc[i, 'coords'].strip("()").split(" ")
    dfa.loc[i, 'longitude'] = float(coords[0])
    dfa.loc[i, 'latitude'] = float(coords[1])
df = dfa.drop(columns=['coords'])

# Create a map centered around the average coordinates
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=13)

# Add a color coded marker for each sensor
for i, row in df.iterrows():
    if row['region'] == regions[0]:
        ico = folium.CustomIcon(
            yellow_marker,
            icon_size=(30,45)
            )
        folium.Marker([row['latitude'], row['longitude']], icon=ico, popup=row['name']).add_to(m)
    elif row['region'] == regions[1]:
        ico = folium.CustomIcon(
            red_marker,
            icon_size=(30,45)
            )
        folium.Marker([row['latitude'], row['longitude']], icon=ico, popup=row['name']).add_to(m)
    elif row['region'] == regions[2]:
        ico = folium.CustomIcon(
            green_marker,
            icon_size=(30,45)
            )
        folium.Marker([row['latitude'], row['longitude']], icon=ico, popup=row['name']).add_to(m)
    else:
        folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)

# Save the map to an HTML file
m.save('map.html')