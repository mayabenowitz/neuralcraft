import os
import sys
ROOT_DIR = os.path.dirname(os.path.abspath('..'))
sys.path.insert(0, os.path.abspath(ROOT_DIR))

import streamlit as st  
import pandas as pd
import numpy as np
import plotly.express as px

from src.visualization.vis import query_prod_growth

st.beta_set_page_config(
    page_title="Neuralcraft",
    page_icon="🧊",
    layout="centered"
)

@st.cache
def load_prod_growth_data():
    df = pd.read_csv(ROOT_DIR+'/data/processed/productivity_growth.csv')
    return df

df = load_prod_growth_data()

def prod_growth_plot(
    df, countries, subject, color="Country", activity=None, trendline=None
):
    user_query = query_prod_growth(countries=countries, subject=subject)
    df = df.query(user_query)

    if trendline is None:
        fig = px.line(
            df, x="Year", y="Value", width=750, template="ggplot2", color=color
        )
        fig.update_layout(
            title={
                    'text': "Productivity Growth in OECD Countries",
                    'y':0.98,
                    'x':0.25,
                    'xanchor': 'center',
                    'yanchor': 'top'
            },
            font = dict(
                family="arial",
                size=14,
            )
        )
        return fig
    if trendline is not None:
        fig = px.scatter(
            df,
            x="Year",
            y="Value",
            width=750,
            template="ggplot2",
            color=color,
            trendline=trendline,
            title="Productivity Growth in OECD Countries"
        )
        return fig

st.title('Can We Solve The Looming Skills Crisis?')
st.markdown("---")
st.sidebar.markdown('### Menu')

countries = df['Country'].unique().tolist()
measures = df['Subject'].unique().tolist()
trendlines = [None, 'ols', 'lowess']

def format_trendlines(x):
    if x == 'ols':
        return 'OLS Linear Regression'
    if x == 'lowess':
        return 'LOWESS'

country_options = st.sidebar.multiselect("Select Countries", countries)
measure_options = st.sidebar.selectbox("Select Measure", measures)
trendline_options = st.sidebar.radio(
    'Select Trendline', 
    trendlines, 
    format_func=format_trendlines
)

# TO DO: 1) if no data available for given country-measure pair display markdown
# 2) give user option to display data dictionary
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
except ValueError:
    st.plotly_chart(
        prod_growth_plot(
            df,
            countries=['G7'], 
            subject='GDP per hour worked, constant prices'
        ),
        use_container_width=False
    )