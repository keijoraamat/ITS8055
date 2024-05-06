import pandas as pd
import folium
import re

filepath ='sensor_positions.csv'

dfa = pd.read_csv(filepath, header=None)


dfa.columns = ['coords', 'name']
print(dfa.tail())
for i, row in dfa.iterrows():
    coords = dfa.loc[i, 'coords'].strip("()").split(" ")
    print(coords)
    dfa.loc[i, 'longitude'] = float(coords[0])
    dfa.loc[i, 'latitude'] = float(coords[1])
df = dfa.drop(columns=['coords'])
print(df.tail())

# Create a map centered around the average coordinates
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=13)

# Add a marker for each sensor
for i, row in df.iterrows():
    #print(f"lat: {row['latitude']}, lng: {row['longitude']}, name: {row['name']}")
    if i <100:
        ico = folium.CustomIcon(icon_size=(50,50))
        folium.Marker([row['latitude'], row['longitude']], icon=ico, popup=row['name']).add_to(m)
    else:
        folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)

# Save the map to an HTML file
m.save('map.html')