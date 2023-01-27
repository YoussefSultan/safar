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

st.session_state['button'] = 'Desktop'

button = st.button(st.session_state['button'])

if not button:
    height, width = 750, 350
else:
    height, width = 800, 1750
    st.session_state['button'] = 'Mobile'
