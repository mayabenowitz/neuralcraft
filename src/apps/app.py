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
    df, countries, subject, kind="line", color="Country", activity=None, trendline=None
):
    user_query = query_prod_growth(countries=countries, subject=subject)
    df = df.query(user_query)

    if kind == "line":
        return px.line(
            df, x="Year", y="Value", width=750, template="ggplot2", color=color
        )

    if kind == "scatter":
        return px.scatter(
            df,
            x="Year",
            y="Value",
            width=750,
            template="ggplot2",
            color=color,
            trendline=trendline,
        )

st.title('Can We Solve The Looming Skills Crisis?')
st.markdown("---")
st.sidebar.markdown('### Menu')

countries = df['Country'].unique().tolist()
options_1 = st.sidebar.multiselect("Select Countries", countries)

try:
    st.plotly_chart(
        prod_growth_plot(
            df,
            kind='line',
            countries=options_1, 
            subject='GDP per hour worked, constant prices',
            trendline='lowess'
        ),
        use_container_width=False
    )
except ValueError:
    st.plotly_chart(
        prod_growth_plot(
            df,
            kind='line',
            countries=['G7'], 
            subject='GDP per hour worked, constant prices',
            trendline='lowess'
        ),
        use_container_width=False
    )