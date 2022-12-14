import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import LocateControl
import pandas as pd
from pandas import DataFrame

st.set_page_config(
    page_title="Safar explore app",
    page_icon="🧊",
    layout='wide')

button = st.button("Desktop")
if not button:
    height, width = 750, 350
else:
    height, width = 800, 1750

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
    linkofplace = ("https://www.google.com/search?q=" + name + ' ' + st.secrets['place_of_interest']).replace(" ","%20")
    try:
        folium.Marker(
            place_loc, tooltip=tooltip, icon=folium.Icon(color=color,icon_color="white"), popup="<a href=_link target='_blank'>link</a>".replace("_link",linkofplace).replace("link",name)
        ).add_to(m)
        
        folium.Icon(color=color)
    except:
        st.error(f"null values found...frozen at {name}")
        st.dataframe(df[df.Longitude.isnull()])
        break

# Add location of user
LocateControl().add_to(m)

st.write("## The Map:")
folium_static(m, height=height,width=width)

c1, c2, c3, c4 = st.columns(4)
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
with c4:
    st.write('### Sites To See 🟧:')
    to_see_df = list(df[df.experienced == 3].formatted_name)
    st.write(to_see_df)
