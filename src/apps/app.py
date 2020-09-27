import os
import sys
ROOT_DIR = os.path.dirname(os.path.abspath('..'))
sys.path.insert(0, os.path.abspath(ROOT_DIR))

import streamlit as st  
import pandas as pd
import numpy as np
import plotly.express as px

from src.visualization.vis import prod_growth_plot, query_prod_growth

@st.cache
def load_prod_growth_data():
    df = pd.read_csv(ROOT_DIR+'/data/processed/productivity_growth.csv')
    return df

df = load_prod_growth_data()
q = query_prod_growth(countries=['United States', 'United Kingdom'], subject='GDP per hour worked, constant prices')
df = df.query(q)

fig = px.line(df, x='Year', y='Value', width=1000, template='ggplot2', color='Country')

st.plotly_chart(
    fig,
    use_container_width=False
)
