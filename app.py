from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pydeck as pdk
from datetime import datetime
import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pydeck as pdk
import ssl

def main():
    df = load_data()
    page = st.sidebar.selectbox("Dashboard", ["Public Dashboard", "Hospital", "---", 'Aceh', 'Bali', 'Banten', 'Babel', 'Bengkulu', 'DIY', 'Jakarta',
                                              'Jambi', 'Jabar', 'Jateng', 'Jatim', 'Kalbar', 'Kaltim', 'Kalteng',
                                              'Kalsel', 'Kaltara', 'Kep Riau', 'NTB', 'Sumsel', 'Sumbar', 'Sulut',
                                              'Sumut', 'Sultra', 'Sulsel', 'Sulteng', 'Lampung', 'Riau', 'Malut',
                                              'Maluku', 'Papbar', 'Papua', 'Sulbar', 'NTT', 'Gorontalo'])
    #pred = st.sidebar.selectbox("Province Predictions", [])

    if page == "Public Dashboard":
        st.header("Public Dashboard 🚑")
        st.write("")
        st.write('Coronavirus secara resmi menjadi pandemi. Sejak kasus pertama pada bulan Desember, penyakit ini telah menyebar dengan cepat ke hampir seluruh penjuru dunia. Mereka mengatakan itu bukan penyakit yang parah tetapi jumlah orang yang membutuhkan perawatan di rumah sakit meningkat secepat kasus baru.')
        st.write("")
        st.write("### Covid Map Indonesia")
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        df_map = pd.read_csv('data-covid-map.csv')

        layer = pdk.Layer(
                "ScatterplotLayer",
                df_map,
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
        view_state = pdk.ViewState(latitude=df_map['latitude'].iloc[-1], longitude=df_map['longitude'].iloc[-1], zoom=3, min_zoom= 1, max_zoom=5)

            # Render
        r = pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/satellite-v9',
                        initial_view_state=view_state, tooltip={"html": "<b>Point ID: </b> {Provinsi} <br /> "
                                                                        "<b> Total Kasus: </b>{Total}"})
        r

        #st.write(df)
        st.write("")

        df_transpose = df.T
        st.write('Total Kasus', df_transpose['2021-01-15'].sum())
        st.write("")
        st.write("")
        if st.checkbox('Show Dataframe'):
            st.write(df)
        if st.checkbox('Show Data Shape'):
            st.write(df.shape)

        if st.checkbox("Show Province"):
            all_columns = df.columns.to_list()
            st.write(all_columns)

        if st.checkbox("Summary"):
            st.write(df.describe())

        # if st.checkbox("Maps"):

         #   data1 = pd.read_csv('data-covid-gps.csv')
         #   st.map(data1)

        all_columns_names = df.columns.tolist()
        type_of_plot = st.selectbox("Select Type of Plot", [
            "area", "bar", "line", "hist", "box", "kde"])
        selected_columns_names = st.multiselect(
            "Select Columns To Plot", all_columns_names)

        if st.button("Generate Plot"):
            st.success("Generating Customizable Plot of {} for {}".format(
                type_of_plot, selected_columns_names))

            # Plot By Streamlit
            if type_of_plot == 'area':
                cust_data = df[selected_columns_names]
                st.area_chart(cust_data)

            elif type_of_plot == 'bar':
                cust_data = df[selected_columns_names]
                st.bar_chart(cust_data)

            elif type_of_plot == 'line':
                cust_data = df[selected_columns_names]
                st.line_chart(cust_data)
            # Custom Plot
            elif type_of_plot:
                cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
                st.write(cust_plot)
                st.pyplot()

    elif page == "Hospital":
        st.header("Hospital Dashboard 🚑")
        st.write("")
        st.write("Data Hospital")
        hospital = pd.read_csv('hospital.csv')
        st.write(hospital)

        if st.checkbox("Filter by Province"):
            province_hospital = hospital.set_index(
                'province').drop_duplicates()
            #all_hospital_region = hospital.province.tolist()
            selected_indices = st.multiselect(
                'Select rows:', province_hospital.index)
            selected_rows = province_hospital.loc[selected_indices]
            st.write('### Selected Rows', selected_rows)

            # host_reg = hospital.loc[hospital['province']== ('Aceh')]
            # st.write(host_reg)
            # print(hospital.loc[hospital['Aceh'] == 'foo'])

    elif page == "Jakarta":
        st.title("LSTM Model Jakarta Cases")
        import jakarta

    elif page == "Aceh":
        st.title("LSTM Model Aceh Cases")
        import aceh
    st.sidebar.subheader("")
    st.sidebar.subheader(
        """Created with 💖 in My Sweet Home on Thesis purposes by [Arvindraj](https://www.linkedin.com/in/arvind-raj-1379371a8/) the data that i used is in the column below
        sinta.ristekbrin.go.id/covid/datasets """)

    #st.sidebar.image('logo.jpg', width=300)

    # cust_data = df[selected_columns_names]
    # st.write(cust_data)


@ st.cache
def load_data():
    df = pd.read_csv('data-covid-clean.csv')
    return df.set_index('date')


if __name__ == "__main__":
    main()
