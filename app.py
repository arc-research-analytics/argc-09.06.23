import streamlit as st
from PIL import Image
import pandas as pd
import geopandas as gpd
import plotly.express as px
import pydeck as pdk

# customize
st.set_page_config(
    page_title="Forsyth County Housing Trends",
    page_icon=":house:",
    initial_sidebar_state="collapsed"
)


# set county variable here ONLY ONCE!!
county_var = 'Forsyth'


# sidebar variables vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

st.sidebar.markdown(
    f"<p style='text-align:center;color:#FFFFFF;font-style:italic;'>Filter housing data by:</p>", unsafe_allow_html=True)
# st.sidebar.write("")

# all the years available for selection
years = st.sidebar.select_slider(
    'Transaction year',
    options=[
        2018,
        2019,
        2020,
        2021,
        2022,
        2023
    ],
    value=(2020, 2023)
)

# dashboard title styling variables
dash_title1_color = '#FFFFFF'
dash_title_font_size = '20'
dash_title1_font_weight = '900'
line_height1 = '12'

dash_title2_color = '#022B3A'
dash_title2_font_weight = '700'
line_height2 = '5'

# dashboard title
st.markdown(f"<p style='color:{dash_title1_color}; font-size:{dash_title_font_size}px; font-weight:{dash_title1_font_weight}; line-height:{line_height1}px; display:in-line; text-align:center;'>{county_var} County Housing Trends</p>", unsafe_allow_html=True)

if years[0] != years[1]:
    st.markdown(
        f"<p style='color:{dash_title2_color}; font-size:{dash_title_font_size}px; font-weight:{dash_title2_font_weight}; line-height:{line_height2}px; display:in-line; text-align:center;'>{years[0]} - {years[1]}</p>", unsafe_allow_html=True)
else:
    st.markdown(
        f"<p style='color:{dash_title2_color}; font-size:{dash_title_font_size}px; font-weight:{dash_title2_font_weight}; line-height:{line_height2}px; display:in-line; text-align:center;'>{years[0]} only</p>", unsafe_allow_html=True)

st.markdown("<p style='font-size:13px; color:#022B3A; font-style:italic; line-height:5px; display:in-line; text-align:center;'>Expand lefthand sidebar to filter housing data.", unsafe_allow_html=True)
st.write("")


# sidebar variables ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


@st.cache_data
def load_tab_data():
    # load the data
    df = pd.read_csv('Fulton_18-23_v2.csv',
                     thousands=',', keep_default_na=False)

    df = df[[
        'Square Ft',
        'year_sale',
        'year_blt',
        'price_sf',
        'salePrice_numeric',
        'Sub_geo',
        'unique_ID',
        'year',
        'month',
        'year-month'
    ]]

    # drop the duplicates that show up in the data
    df = df.drop_duplicates(subset='unique_ID')

    # return this item
    return df


def filter_data():
    df = load_tab_data()

    # year filter
    if years[0] != years[1]:
        df = df[(df['year_sale'] >= years[0]) & (df['year_sale'] <= years[1])]
    else:
        df = df[df['year_sale'] == years[0]]

    # now group by sub geography
    grouped_df = df.groupby('Sub_geo').agg({
        'price_sf': 'median',
        'salePrice_numeric': 'median',
        'year_blt': 'median',
        'unique_ID': 'count',
    }).reset_index()

    return filtered_df, grouped_df, filtered_df_map_KPI, df_KPI_delta0, df_KPI_delta1


# colors to be used in the mapping functions
custom_colors = [
    '#97a3ab',  # lightest blue
    '#667883',
    '#37505d',
    '#022b3a'  # darkest blue
]

# convert the above hex list to RGB values
custom_colors = [tuple(int(h.lstrip('#')[i:i+2], 16)
                       for i in (0, 2, 4)) for h in custom_colors]

# map variables
map_lat_2D = 33.84552225888502
map_lat_3D = 34.978
map_long = -84.45
map_height = 330
map_zoom_2D = 8.0  # higher numeric value = 'zooming in'
map_zoom_3D = 6  # higher numeric value = 'zooming in'


def mapper_2D():

    # tabular data
    df = filter_data()[1]
    # df['GEOID'] = df['GEOID'].astype(str)

    # read in geospatial
    gdf = gpd.read_file('Geography/Fulton_neighborhoods.gpkg')

    # join together the 2, and let not man put asunder
    joined_df = gdf.merge(df, left_on='Sub-geo', right_on='Sub_geo')

    # ensure we're working with a geodataframe
    joined_df = gpd.GeoDataFrame(joined_df)

    # format the column to show the price / SF
    joined_df['price_sf_formatted'] = joined_df['price_sf'].apply(
        lambda x: "${:.0f}".format((x)))

    # format the column to show the overall price
    joined_df['price_formatted'] = joined_df['salePrice_numeric'].apply(
        lambda x: "${:,.0f}".format((x)))

    # add 1,000 separator to column that will show total sales
    joined_df['total_sales'] = joined_df['unique_ID'].apply(
        lambda x: '{:,}'.format(x))

    # set choropleth color
    joined_df['choro_color'] = pd.cut(
        joined_df['price_sf'],
        bins=len(custom_colors),
        labels=custom_colors,
        include_lowest=True,
        duplicates='drop'
    )

    # create map intitial state
    initial_view_state = pdk.ViewState(
        latitude=map_lat_2D,
        longitude=map_long,
        zoom=map_zoom_2D,
        max_zoom=15,
        min_zoom=8,
        pitch=0,
        bearing=0,
        height=map_height
    )

    geojson = pdk.Layer(
        "GeoJsonLayer",
        joined_df,
        pickable=True,
        autoHighlight=True,
        highlight_color=[255, 137, 102, 100],
        opacity=0.7,
        stroked=True,
        filled=True,
        get_fill_color='choro_color',
        get_line_color=[0, 0, 0, 255],
        line_width_min_pixels=1
    )

    tooltip = {
        "html": "Median price per SF: <b>{price_sf_formatted}</b><br>\
                    Median price: <b>{price_formatted}</b><br>\
                    Total sales: <b>{total_sales}</b><br>\
                    City/Region: <b>{Sub-geo}</b>",
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
        map_provider='mapbox',
        map_style=base_map_dict[base_map],
        tooltip=tooltip)

    return r


def mapper_3D():

    # tabular data
    df = filter_data()[1]
    # df['GEOID'] = df['GEOID'].astype(str)

    # read in geospatial
    gdf = gpd.read_file('Geography/Fulton_neighborhoods.gpkg')

    # join together the 2, and let not man put asunder
    joined_df = gdf.merge(df, left_on='Sub-geo', right_on='Sub_geo')

    # ensure we're working with a geodataframe
    joined_df = gpd.GeoDataFrame(joined_df)

    # format the column to show the price / SF
    joined_df['price_sf_formatted'] = joined_df['price_sf'].apply(
        lambda x: "${:.0f}".format((x)))

    # format the column to show the overall price
    joined_df['price_formatted'] = joined_df['salePrice_numeric'].apply(
        lambda x: "${:,.0f}".format((x)))

    # add 1,000 separator to column that will show total sales
    joined_df['total_sales'] = joined_df['unique_ID'].apply(
        lambda x: '{:,}'.format(x))

    # set choropleth color
    joined_df['choro_color'] = pd.cut(
        joined_df['price_sf'],
        bins=len(custom_colors),
        labels=custom_colors,
        include_lowest=True,
        duplicates='drop'
    )

    # set initial view state
    initial_view_state = pdk.ViewState(
        latitude=map_lat_3D,
        longitude=map_long,
        zoom=map_zoom_3D,
        max_zoom=15,
        min_zoom=5,
        pitch=45,
        bearing=0,
        height=map_height
    )

    # create geojson layer
    geojson = pdk.Layer(
        "GeoJsonLayer",
        joined_df,
        pickable=True,
        autoHighlight=True,
        highlight_color=[255, 137, 102, 100],
        opacity=0.7,
        stroked=False,
        filled=True,
        wireframe=False,
        extruded=True,
        get_elevation='unique_ID * 50',
        get_fill_color='choro_color',
        get_line_color='choro_color',
        line_width_min_pixels=1
    )

    tooltip = {
        "html": "Median price per SF: <b>{price_sf_formatted}</b><br>\
                    Median price: <b>{price_formatted}</b><br>\
                    Total sales: <b>{total_sales}</b><br>\
                    City/Region: <b>{Sub-geo}</b>",
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
        map_provider='mapbox',
        map_style=base_map_dict[base_map],
        tooltip=tooltip)

    return r


def charter():
    # test chart
    df = filter_data()[0]

    df_grouped = df.groupby('year-month').agg({
        'price_sf': 'median',
        'unique_ID': 'count',
        'month': pd.Series.mode,
        'year': pd.Series.mode,
    }).reset_index()

    # sort the data so that it's chronological
    df_grouped = df_grouped.sort_values(['year', 'month'])

    fig = px.line(
        df_grouped,
        x="year-month",
        y='price_sf',
        custom_data=['unique_ID']
    )

    # modify the line itself
    fig.update_traces(
        mode="lines",
        line_color='#022B3A',
        hovertemplate="<br>".join([
            # "<b>%{x}</b><br>",
            "Median price / SF: <b>%{y}</b>",
            "Total sales: <b>%{customdata[0]:,.0f}</b>"
        ])
    )

    # set chart title style variables
    chart_title_font_size = '17'
    chart_title_color = '#FFFFFF'
    chart_title_font_weight = '650'

    chart_subtitle_font_size = '14'
    chart_subtitle_color = '#022B3A'
    chart_subtitle_font_weight = '650'

    if sub_geo == "":
        chart_title_text = "Countywide home prices per month"
    elif len(sub_geo) == 1:
        chart_title_text = f"{sub_geo[0]} home prices per month"
    else:
        chart_title_text = f"Prices per month for selected regions"

    # update the fig
    fig.update_layout(
        title_text=f'<span style="font-size:{chart_title_font_size}px; font-weight:{chart_title_font_weight}; color:{chart_title_color}">{chart_title_text}</span><br><span style="font-size:{chart_subtitle_font_size}px; font-weight:{chart_subtitle_font_weight}; color:{chart_subtitle_color}"><i>Orange lines reflect range of selected years</i></span>',
        title_x=0,
        title_y=0.93,
        margin=dict(
            t=85
        ),
        hoverlabel=dict(
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#022B3A",
            font_size=16,  # set the font size of the chart tooltip
            font_color="#022B3A",
            align="left"
        ),
        yaxis=dict(
            linecolor="#022B3A",
            title=None,
            tickfont_color='#022B3A',
            tickfont_size=13,
            tickformat='$.0f',
            showgrid=False,
            fixedrange=True
        ),
        xaxis=dict(
            linecolor="#022B3A",
            linewidth=1,
            tickfont_color='#022B3A',
            title=None,
            tickangle=90,
            tickfont_size=13,
            tickformat='%b %Y',
            dtick='M7',
            fixedrange=True
        ),
        height=460,
        hovermode="x unified")

    # add shifting vertical lines
    year_start = {
        2018: '2018-1',
        2019: '2019-1',
        2020: '2020-1',
        2021: '2021-1',
        2022: '2022-1',
        2023: '2023-1'
    }

    year_end = {
        2018: '2018-12',
        2019: '2019-12',
        2020: '2020-12',
        2021: '2021-12',
        2022: '2022-12',
        2023: '2023-4'
    }

    fig.add_vline(x=year_start[years[0]], line_width=2,
                  line_dash="dash", line_color="#FF8966")
    fig.add_vline(x=year_end[years[1]], line_width=2,
                  line_dash="dash", line_color="#FF8966")

    return fig


if sub_geo == "":
    st.markdown(f"<p style='color:#FFFFFF; font-size:17px; font-weight:800; line-height:15px; display:in-line; text-align:left;'>Countywide median price / SF</p>", unsafe_allow_html=True)
elif len(sub_geo) == 1:
    st.markdown(
        f"<p style='color:#FFFFFF; font-size:17px; font-weight:800; line-height:15px; display:in-line; text-align:left;'>{sub_geo[0]} sales price / SF</p>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='color:#FFFFFF; font-size:17px; font-weight:800; line-height:15px; display:in-line; text-align:left;'>Sales price / SF for selected regions</p>", unsafe_allow_html=True)


# map
if map_view == '2D':
    st.pydeck_chart(mapper_2D(), use_container_width=True)
else:
    st.pydeck_chart(mapper_3D(), use_container_width=True)
    st.markdown("<span style='color:#022B3A'>Shift + click to change map angle & rotation. City/Region 'height' represents total sales; darker shading represents greater median sales price / SF.</span>", unsafe_allow_html=True)

# chart
st.plotly_chart(charter(), use_container_width=True,
                config={'displayModeBar': False})


# kpi values
total_sales = '{:,.0f}'.format(filter_data()[1]['unique_ID'].sum())
median_price_SF = '${:.0f}'.format(filter_data()[2]['price_sf'].median())
median_price = '${:,.0f}'.format(
    filter_data()[2]['salePrice_numeric'].median())
med_vintage = '{:.0f}'.format(filter_data()[2]['year_blt'].median())
med_SF = '{:,.0f}'.format(filter_data()[2]['Square Ft'].median())
YoY_delta = '{0:.1%}'.format((filter_data()[4]['price_sf'].median(
) - filter_data()[3]['price_sf'].median()) / filter_data()[3]['price_sf'].median())

# kpi styles
KPI_font_size = '20'
KPI_font_weight = '700'  # thickness of the bold
KPI_label_font_color = '#FFFFFF'
KPI_value_font_color = '#022B3A'
KPI_line_height = '25'  # vertical spacing between the KPI label and value


# KPI tyme
# subcol1, subcol2 = st.columns([1, 1])

# first metric - "Total sales"
st.markdown(f"<p style='color:{KPI_label_font_color}; font-size:{KPI_font_size}px; font-weight:{KPI_font_weight}; line-height:{KPI_line_height}px; display:in-line; text-align:center;'>Total home sales: <span style='color:{KPI_value_font_color};'>{total_sales}</span></p>", unsafe_allow_html=True)

# second metric - "Median price"
st.markdown(f"<p style='color:{KPI_label_font_color}; font-size:{KPI_font_size}px; font-weight:{KPI_font_weight}; line-height:{KPI_line_height}px; display:in-line; text-align:center;'>Median sale price: <span style='color:{KPI_value_font_color};'>{median_price}</span></p>", unsafe_allow_html=True)

# third metric - "Median vintage"
st.markdown(f"<p style='color:{KPI_label_font_color}; font-size:{KPI_font_size}px; font-weight:{KPI_font_weight}; line-height:{KPI_line_height}px; display:in-line; text-align:center;'>Median vintage: <span style='color:{KPI_value_font_color};'>{med_vintage}</span></p>", unsafe_allow_html=True)

# fourth metric - "Median SF"
st.markdown(f"<p style='color:{KPI_label_font_color}; font-size:{KPI_font_size}px; font-weight:{KPI_font_weight}; line-height:{KPI_line_height}px; display:in-line; text-align:center;'>Median size (SF): <span style='color:{KPI_value_font_color};'>{med_SF}</span></p>", unsafe_allow_html=True)

# delta KPI, resting under the 4 KPIs above
if years[0] != years[1]:
    st.markdown(
        f"<p style='color:{KPI_label_font_color}; font-size: {KPI_font_size}px; font-weight:{KPI_font_weight}; line-height:{KPI_line_height}px; display:in-line; text-align:center;'>Change in median price / SF <br>({years[0]} - {years[1]}): <span style='color:{KPI_value_font_color};'>{YoY_delta}</span></p>", unsafe_allow_html=True)
else:
    st.markdown(
        f"<span style='color:{KPI_label_font_color}; font-size: {KPI_font_size}px; font-weight:{KPI_font_weight}; display:flex; justify-content:center;'>No year over year change.</span>", unsafe_allow_html=True)


# map notes
if map_view == '2D':
    expander = st.expander("Notes")
    expander.markdown(
        f"<span style='color:#022B3A'> Darker shades of Census tracts on map represent higher sales prices per SF for the selected time period. Dashboard excludes non-qualified, non-market, and bulk transactions. Excludes transactions below $1,000, homes smaller than 75 square feet, and transactions with missing values. Data downloaded from {county_var} County public records on July 24, 2023, and is assumed to be accurate and reliable.</span>", unsafe_allow_html=True)
else:
    expander = st.expander("Notes")
    expander.markdown(
        f"<span style='color:#022B3A'>Census tract 'height' representative of total sales per tract. Darker shades of Census tracts on map represent higher sales prices per SF for the selected time period. Dashboard excludes non-qualified, non-market, and bulk transactions. Excludes transactions below $1,000, homes smaller than 75 square feet, and transactions with missing values. Data downloaded from {county_var} County public records on May 11, 2023 and is assumed to be accurate and reliable.</span>", unsafe_allow_html=True)

# Draw ARC logo at the bottom of the page
im = Image.open('content/logo.png')
subcol1, subcol2, subcol3 = st.columns([1.4, 1, 1])
subcol2.write(f"Powered by:")
subcol2.image(im, width=80)
