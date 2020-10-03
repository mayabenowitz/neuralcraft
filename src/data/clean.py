import sys
import os
import pandas as pd
import numpy as np

dirname = os.path.dirname(os.path.abspath(".."))

def clean_lpc_data(
    input_filepath=dirname+'/data/raw/lpc_by_industry.csv',
    output_filepath=dirname+"/data/processed/lpc_by_industry.csv",
):
    df = pd.read_csv(input_filepath, low_memory=False)

    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)

    ids = df.iloc[:, 0:5].columns.tolist()
    values = df.iloc[:, 5:38].columns.tolist()
    values = [str(int(i)) for i in values]
    df.columns = ids + values

    df = pd.melt(df, id_vars=ids, value_vars=values, var_name="Year")
    df.dropna(inplace=True)
    df.drop(columns=["Industry Digit"], inplace=True)

    df["Industry"] = (
        df["Industry"]
        .str.replace("-", "")
        .map(lambda s: "".join([i for i in s if not i.isdigit()]))
    )

    df["Industry Sector"] = (
        df["Industry Sector"]
        .str.replace("-", "")
        .map(lambda s: "".join([i for i in s if not i.isdigit()]))
    )

    df["value"] = df["value"].replace("n.a.", np.nan)
    df["Year"] = df["Year"].astype(int)

    df["Industry"] = df["Industry"].map(lambda s: s.lstrip(" "))
    df["Industry Sector"] = df["Industry Sector"].map(
        lambda s: s.lstrip(" ").lstrip(", ")
    )

    df.to_csv(output_filepath, index=False)


def clean_prod_growth_ind_data(input_filepath, output_filepath):
    df = pd.read_csv(input_filepath)
    df.drop(
        columns=[
            "LOCATION",
            "SUBJECT",
            "MEASURE",
            "ACTIVITY",
            "TIME",
            "Unit Code",
            "PowerCode Code",
            "PowerCode",
            "Reference Period Code",
            "Reference Period",
            "Flag Codes",
            "Flags",
        ],
        inplace=True,
    )

    df.rename(columns={'Time': 'Year'}, inplace=True)
    df["Subject"] = df["Subject"].map(lambda s: s.strip(" "))
    df["Activity"] = df["Activity"].map(lambda s: s.strip(" "))
    df["Year"].astype(int)
    df.to_csv(output_filepath, index=False)


def clean_prod_growth_data(input_filepath, output_filepath):
    df = pd.read_csv(input_filepath)
    df.drop(
        columns=[
            "LOCATION",
            "SUBJECT",
            "MEASURE",
            "TIME",
            "Unit Code",
            "PowerCode Code",
            "PowerCode",
            "Reference Period Code",
            "Reference Period",
            "Flag Codes",
            "Flags",
        ],
        inplace=True,
    )

    df.rename(columns={'Time': 'Year'}, inplace=True)
    df["Subject"] = df["Subject"].map(lambda s: s.strip(" "))
    df["Year"].astype(int)
    df.to_csv(output_filepath, index=False)


def clean_gdp_data(input_filepath, output_filepath):
    df = pd.read_csv(input_filepath)
    df.drop(
        columns=[
            'LOCATION',
            'SUBJECT',
            'MEASURE',
            'TIME',
            'Unit Code',
            'Unit',
            'PowerCode Code',
            'PowerCode',
            'Reference Period Code',
            'Reference Period',
            'Flag Codes',
            'Flags'


        ],
        inplace=True
    )
    df.rename(columns={'Time': 'Year'}, inplace=True)
    df['Year'].astype(int)
    df.to_csv(output_filepath, index=False)
    

if __name__ == "__main__":
    print('Cleaning data...')
    clean_lpc_data()
    clean_prod_growth_data(
        input_filepath=dirname+'/data/raw/productivity_growth.csv', 
        output_filepath=dirname+'/data/processed/productivity_growth.csv'
    )
    clean_prod_growth_ind_data(
        input_filepath=dirname+'/data/raw/productivity_growth_by_industry.csv',
        output_filepath=dirname+'/data/processed/productivity_growth_by_industry.csv'
    )
    clean_gdp_data(
        input_filepath=dirname+'/data/raw/gdp_per_capita.csv',
        output_filepath=dirname+'/data/processed/gdp_per_capita.csv'
    )
    print('Data cleaned!')