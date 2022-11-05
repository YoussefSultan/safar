import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from pandas import DataFrame

#@st.cache(ttl=10)
exec(open("get_details.py").read())
exec(open("update_sheets.py").read())

col1, col2, col3, col4, col5, col6 = st.columns((5,1,1,1,1,2))

destination_loc = [43.653226, -79.3831843]

# center on Liberty Bells
m = folium.Map(location=destination_loc, zoom_start=13)
with col1:
    st.write("## The Map:")
    with col6:
        st.write("#### Places experienced:")
    for i in range(len(df)):
        name = df.loc[i,'formatted_name']
        Lon = df.loc[i,'Longitude']
        Lat = df.loc[i,'Latitude']
        city = df.loc[i,'city']
        Rating = df.loc[i,'rating']
        experienced = df.loc[i,'experienced']

        place_loc = [Lon,Lat]
        if experienced == 0:
            color = "darkblue"
        elif experienced == 1:
            with col6:
                st.write("- " + str(name))
                color = "red"
        else:
            with col6:
                st.write("#### New places added:")
                st.write("- ", str(name))
                color = 'green'
        tooltip = str(name) + " | Rating: " + str(Rating)
        try:
            folium.Marker(
                place_loc, popup=name, tooltip=tooltip, icon=folium.Icon(color=color,icon_color="white")
            ).add_to(m)
            
            folium.Icon(color=color)
        except:
            st.error(f"null values found...frozen at {name}")
            st.dataframe(df[df.Longitude.isnull()])
            break
    # call to render Folium map in Streamlit
    folium_static(m, height=700,width=500)
