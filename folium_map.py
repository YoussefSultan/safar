# Take median of all longitudinal data for map view from users data
destination_loc = [float(df.Longitude.median()),float(df.Latitude.median())]

# Center on longitude and latitude coordinates and zoom settings
m = folium.Map(location=destination_loc, zoom_start=13)

# Create list to add places experienced data
exp = []

# loop through each record of the dataframe,
# for each record pinpoint the metadata to the folium map

for i in range(len(df)):
    
    # Record all of data for each column in variables to pass on
    name = df.loc[i,'formatted_name']
    Lon = df.loc[i,'Longitude']
    Lat = df.loc[i,'Latitude']
    city = df.loc[i,'city']
    Rating = df.loc[i,'rating']
    experienced = df.loc[i,'experienced']
    notes = df.loc[i,'notes']
    place_loc = [Lon,Lat]

    # set color of marker based experience column,
    # >> 0: Not Experienced, 1: Experienced, all other numbers: Not experienced color coded differently incase a friend has their own points, 3: Used to identify landmarks
    if experienced == 0:
        color = "darkblue"
    elif experienced == 1:
        exp.append(str(name))
        color = "red"
    elif experienced == 3:
        color = "orange"
    else:
        color = 'green'
    
    # Adjust tool tip for each marker with metadata and link of place
    tooltip = str(name) + " | Rating: " + str(Rating) + " | Notes: " + str(notes)
    linkofplace = ("https://www.google.com/search?q=" + name + ' ' + users_place_of_interest).replace(" ","%20")
    
    # pinpoint marker; adds all metadata to map
    try:
        folium.Marker(
            place_loc, tooltip=tooltip, icon=folium.Icon(color=color,icon_color="white"), popup="<a href=_link target='_blank'>link</a>".replace("_link",linkofplace).replace("link",name)
        ).add_to(m)
        
        folium.Icon(color=color)
    except:
        st.error(f"null values found...frozen at {name}")
        st.dataframe(df[df.Longitude.isnull()])
        break

# Add location of user feature
LocateControl().add_to(m)

col1, col2, col3 = st.columns(3)

# Effects how the map is shown based on the mode:
if st.session_state['button'] == 'Mobile':
        # Add map created
    st.write("## The Map:")
    folium_static(m, height=height,width=width)
else:
    with col1:
        # Add map created
        st.write("## The Map:")
        folium_static(m, height=height,width=width)
