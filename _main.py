import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from pandas import DataFrame



button = st.button("Mobile")
if button:
    height, width = 1280, 720
    st.set_page_config(
    page_title="Safar explore app",
    page_icon="🧊",
    layout='centered')
else:
    height, width = 800, 1750
    st.set_page_config(
    page_title="Safar explore app",
    page_icon="🧊",
    layout='wide')

#@st.cache(ttl=10)
exec(open("get_details.py").read())
exec(open("update_sheets.py").read())

destination_loc = [float(df.Longitude.median()),float(df.Latitude.median())]

# center on Liberty Bells
m = folium.Map(location=destination_loc, zoom_start=13)
#with col1:

#st.write("#### Places experienced:")
exp = []
for i in range(len(df)):
    name = df.loc[i,'formatted_name']
    Lon = df.loc[i,'Longitude']
    Lat = df.loc[i,'Latitude']
    city = df.loc[i,'city']
    Rating = df.loc[i,'rating']
    experienced = df.loc[i,'experienced']
    notes = df.loc[i,'notes']

    place_loc = [Lon,Lat]
    if experienced == 0:
        color = "darkblue"
    elif experienced == 1:
        exp.append(str(name))
        color = "red"
    elif experienced == 3:
        color = "orange"
    else:
        color = 'green'
    tooltip = str(name) + " | Rating: " + str(Rating) + " | Notes: " + str(notes)
    try:
        folium.Marker(
            place_loc, popup=name, tooltip=tooltip, icon=folium.Icon(color=color,icon_color="white")
        ).add_to(m)
        
        folium.Icon(color=color)
    except:
        st.error(f"null values found...frozen at {name}")
        st.dataframe(df[df.Longitude.isnull()])
        break

st.write("## The Map:")
folium_static(m, height=height,width=width)

c1, c2, c3= st.columns(3)
with c1:
    st.write('### Experienced 🟥:')
    st.write(exp)
with c2:
    st.write('### Not Experienced 🟦:')
    not_experienced_df = list(df[df.experienced == 0].formatted_name)
    st.write(not_experienced_df)
with c3:
    st.write('### Newly Added 🟩:')
    newly_added_df = list(df[df.experienced == 2].formatted_name)
    st.write(newly_added_df)
