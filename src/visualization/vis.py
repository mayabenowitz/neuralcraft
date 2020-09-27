import pandas as pd
import plotly.express as px


def query_prod_growth(countries, subject):
    country_query = " | ".join([f"(Country == '{i}')" for i in countries])
    subject_query = f"(Subject == '{subject}')"
    return "(" + country_query + ")" + " & " + "(" + subject_query + ")"


def prod_growth_plot(
    df, countries, subject, kind="line", color="Country", activity=None, trendline=None
):
    user_query = query_prod_growth(countries=countries, subject=subject)
    df = df.query(user_query)

    if kind == "line":
        fig = px.line(
            df, x="Year", y="Value", width=1000, template="ggplot2", color=color
        )
        fig.show()
    if kind == "scatter":
        fig = px.scatter(
            df,
            x="Year",
            y="Value",
            width=1000,
            template="ggplot2",
            color=color,
            trendline=trendline,
        )
        fig.show()
