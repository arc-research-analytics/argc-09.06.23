# import libraries
import streamlit as st
import pydeck as pdk
import pandas as pd
import geopandas as gpd

# customize a few items
st.set_page_config(
    page_title="Streamlit demo",
    page_icon=":house:",
    initial_sidebar_state="expanded"
)

# sidebar title
st.sidebar.markdown(
    f"<p style='text-align:center;color:#FFFFFF;font-style:italic;'>Filter housing data by:</p>", unsafe_allow_html=True)

# sidebar slider (year filter)
years = st.sidebar.select_slider(
    'Transaction year',
    options=[
        2018,
        2019,
        2020,
        2021,
        2022
    ],
    value=(2020, 2022),
    help='Filter sales by transaction year.'
)

# main page title
if years[0] != years[1]:
    st.markdown(
        f"<h2 style='color:#FFFFFF; font-weight: 900;'>Forsyth County Housing Trends | <span style='color:#022B3A; font-weight: 400'>{years[0]} - {years[1]}</span></h2>", unsafe_allow_html=True)
else:
    st.markdown(
        f"<h2 style='color:#FFFFFF; font-weight: 900;'>Forsyth County Housing Trends | <span style='color:#022B3A; font-weight: 400'>{years[0]} only</span></h2>", unsafe_allow_html=True)


def filter_data():

    # read in data
    df = pd.read_csv('Data/Final/FullSet_joined.csv',
                     keep_default_na=False,
                     dtype={
                         'GEOID': str
                     })

    # clean up dataframe
    df.drop(columns='Unnamed: 0', inplace=True)

    # apply filter based on the sidebar slider
    if years[0] != years[1]:
        df = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])]
    else:
        df = df[df['Year'] == years[0]]

    return df


def map_viz():

    # define a color ramp
    colors_hex = [
        '#97a3ab',  # lightest blue
        '#667883',
        '#37505d',
        '#022b3a'  # darkest blue
    ]

    # convert to RGB values for the choropleth map
    colors_rgb = [tuple(int(h.lstrip('#')[i:i+2], 16)
                        for i in (0, 2, 4)) for h in colors_hex]

    # Run a groupby method on each Census tract
    df_grouped = df.groupby('GEOID')['price_sf'].median().reset_index()

    # read in geospatial
    gdf = gpd.read_file('Data/Final/ForsythCTs.gpkg',
                        dtype={
                            'GEOID': str
                        })

    # create a new GeoPandas GeoDataFrame by merging above 2 dataframes
    map_gdf = gpd.GeoDataFrame(
        gdf.merge(df_grouped, left_on='GEOID', right_on='GEOID'))

    # format the column to show the price
    map_gdf['price_sf_formatted'] = map_gdf['price_sf'].apply(
        lambda x: "${:,.0f}".format((x)))

    # set choropleth color
    map_gdf['choro_color'] = pd.cut(
        map_gdf['price_sf'],
        bins=len(colors_rgb),
        labels=colors_rgb,
        include_lowest=True,
        duplicates='drop'
    )

    # create map intitial state
    initial_view_state = pdk.ViewState(
        latitude=34.207054643497315,
        longitude=-84.10535919531371,
        zoom=9.2,
        max_zoom=15,
        min_zoom=8,
        pitch=0,
        bearing=0,
        height=565
    )

    geojson = pdk.Layer(
        "GeoJsonLayer",
        map_gdf,
        pickable=True,
        autoHighlight=True,
        highlight_color=[255, 255, 255, 80],
        opacity=0.5,
        stroked=True,
        filled=True,
        get_fill_color='choro_color',
        get_line_color=[0, 0, 0, 255],
        line_width_min_pixels=1
    )

    tooltip = {
        "html": "Median price per SF: <b>{price_sf_formatted}</b><br>",
        "style": {"background": "rgba(2,43,58,0.7)",
                  "border": "1px solid white",
                  "color": "white",
                  "font-family": "Helvetica",
                  "text-align": "center"
                  },
    }

    r = pdk.Deck(
        layers=geojson,
        initial_view_state=initial_view_state,
        map_style=pdk.map_styles.MAPBOX_LIGHT,
        tooltip=tooltip)

    return r


# instantiate the initial dataframe
df = filter_data()

# look at dynamic dataframe in browswer to see if filter is working
st.dataframe(df, use_container_width=True)

# # render the map to the web app
# st.pydeck_chart(map_viz(), use_container_width=True)

# Dynamically show the rows and columns that are being filtered in Streamlit.
st.write(
    f'The filtered data is returning {df.shape[0]:,} sales.')
