import streamlit as st
import pydeck as pdk
import pandas as pd
import ssl

    # get rid of ssl connection error (certificates)
try:
        _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
        pass
else:
        ssl._create_default_https_context = _create_unverified_https_context

st.header("Map data")
# read in data
df = pd.read_csv('data-covid-map.csv')

layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        pickable=True,
        opacity=0.8,
        filled=True,
        radius_scale=2,
        radius_min_pixels=10,
        radius_max_pixels=500,
        line_width_min_pixels=0.01,
        get_position='[longitude, latitude]',
        get_fill_color=[255, 0, 0],
        get_line_color=[0, 0, 0],
    )

    # Set the viewport location
view_state = pdk.ViewState(latitude=df['latitude'].iloc[-1], longitude=df['longitude'].iloc[-1], zoom=3, min_zoom= 1, max_zoom=5)

    # Render
r = pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/satellite-v9',
                 initial_view_state=view_state, tooltip={"html": "<b>Point ID: </b> {Provinsi} <br /> "
                                                                 "<b> Total Kasus: </b>{Total}"})
r

