import os
import sys
ROOT_DIR = os.path.dirname(os.path.abspath('..'))
sys.path.insert(0, os.path.abspath(ROOT_DIR))

from pathlib import Path
import base64

import streamlit as st  
import pandas as pd
import numpy as np
import plotly.express as px

from src.visualization.vis import query_prod_growth

st.beta_set_page_config(
    layout="centered",
    page_icon = "🌌"
)


def _max_width_():
    max_width_str = f"max-width: 950px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

@st.cache
def load_prod_growth_data():
    df = pd.read_csv(ROOT_DIR+'/data/processed/productivity_growth.csv')
    return df


@st.cache
def load_gdp_data():
    df = pd.read_csv(ROOT_DIR+'/data/processed/gdp_per_capita.csv')
    return df

# load dataframes and name them
df_prod = load_prod_growth_data()
df_gdp = load_gdp_data()
df_prod.name = 'Productivity Growth'
df_gdp.name = 'GDP Per Capita'
datasets = {df_prod.name: df_prod, df_gdp.name: df_gdp}

# lineplots and scatterplots
def prod_growth_plot(
    df, countries, subject, color="Country", activity=None, trendline=None
):
    user_query = query_prod_growth(countries=countries, subject=subject)
    name = df.name
    df = df.query(user_query)
    df.name = name

    if trendline is None:
        fig = px.line(
            df, x="Year", y="Value", width=950, template="ggplot2", color=color
        )
    
    if trendline is not None:
        fig = px.scatter(
            df,
            x="Year",
            y="Value",
            width=950,
            template="ggplot2",
            color=color,
            trendline=trendline
        )
    
    if df.name == 'Productivity Growth':
        fig.update_layout(
                title={
                        'text': "Productivity Growth in OECD Countries",
                        'y':.98,
                        'x':0.25,
                        'xanchor': 'center',
                        'yanchor': 'top'
                },
                yaxis_title="Annual Change",
                yaxis=dict(ticksuffix="%"),
                font = dict(
                    family="arial",
                    size=14,
                ),
                hovermode='x',
                colorway = ["#36B0FF"]
            )
    if df.name == 'GDP Per Capita':
        subject = df['Subject'].unique()[0]
        fig.update_layout(
            title={
                    'text': f"{subject}",
                    'y':.98,
                    'x':0.25,
                    'xanchor': 'center',
                    'yanchor': 'top'
            },
            yaxis_title="USD, Current Prices",
            font = dict(
                family="arial",
                size=14,
            ),
            hovermode='x'
        )
    return fig


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def render_svg(svg_file):

    with open(svg_file, "r") as f:
        lines = f.readlines()
        svg = "".join(lines)

        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
        return html

# logo_html = """<img src='data:image/png;base64,{}' class='img-fluid'></p>
#             """.format(img_to_bytes("logo3.png"))

logo_html = render_svg('logo3.svg')

st.title('How The Looming Productivity Crisis Will Reshape Our World.')
st.markdown("---")
st.sidebar.markdown(logo_html, unsafe_allow_html=True)
st.sidebar.markdown('---')
st.sidebar.markdown('### Menu')

def format_trendlines(x):
    if x == 'ols':
        return 'OLS Linear Regression'
    if x == 'lowess':
        return 'LOWESS'

# plotly chart + streamlit sidebar widgets
# TO DO: give user option to display data dictionary
def prod_landing_app(dataset):
    df = datasets[dataset]
    df.name = dataset
    name = df.name

    if df.name == 'GDP Per Capita':
        df = df[df['Measure'] == 'USD, current prices, current PPPs']
        df.name = name

    countries = df['Country'].unique().tolist()
    measures = df['Subject'].unique().tolist()
    measures.insert(0, measures[3])
    measures.pop(4)
    trendlines = [None, 'ols', 'lowess']

    country_options = st.sidebar.multiselect("Select Countries", countries, default=['G7'])
    measure_options = st.sidebar.selectbox("Select Y-axis", measures)
    trendline_options = st.sidebar.radio(
        'Select Trendline', 
        trendlines, 
        format_func=format_trendlines
    )

    try:
        try:
            st.plotly_chart(
                prod_growth_plot(
                    df,
                    countries=country_options, 
                    subject=measure_options,
                    trendline=trendline_options
                ),
                use_container_width=False
            )
        except KeyError:
            st.error('Sorry No Data is Available!')
    except ValueError:
        if len(country_options) == 0:
            st.error('You don\'t have a country selected, silly!')

dataset_options = st.sidebar.selectbox(
    "Select Dataset", 
    list(datasets.keys())
)
prod_landing_app(dataset_options)
    


