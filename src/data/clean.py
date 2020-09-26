
import pandas as pd
import numpy as np


def clean_lpc_data() -> pd.DataFrame:
    df = pd.read_csv(
        '../data/raw/lpc_by_industry.csv',
        low_memory=False 
    )

    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)
    
    ids = df.iloc[:, 0:5].columns.tolist()
    values = df.iloc[:, 5:38].columns.tolist()
    values = [str(int(i)) for i in values]
    df.columns = ids + values

    df = pd.melt(df, id_vars=ids, value_vars=values, var_name='Year')
    df.dropna(inplace=True)
    df.drop(columns=['Industry Digit'], inplace=True)
    
    df['Industry'] = df['Industry']\
        .str.replace('-', '')\
        .map(lambda s: ''.join([i for i in s if not i.isdigit()]))
    
    df['Industry Sector'] = df['Industry Sector']\
        .str.replace('-', '')\
        .map(lambda s: ''.join([i for i in s if not i.isdigit()]))
        
    df['value'] = df['value'].replace('n.a.', np.nan)
    df['Year'] = df['Year'].astype(int)

    df['Industry'] = df['Industry'].map(lambda s: s.lstrip(' '))
    df['Industry Sector'] = df['Industry Sector']\
        .map(lambda s: s.lstrip(' ').lstrip(', '))

    return df

    
def clean_prod_growth_data(path) -> pd.DataFrame:
    """Cleans the productivity_growth.csv and 
    productivity_growth_by_industry.csv datasets
        
    Params
    -------
    path: '../data/raw/productivity_growth.csv' or
    '../data/raw/productivity_growth_by_industry.csv'
    """
    
    df = pd.read_csv(path)
    df.drop(
    columns=[
        'LOCATION',
        'SUBJECT',
        'MEASURE',
        'ACTIVITY',
        'TIME',
        'Unit Code',
        'PowerCode Code',
        'PowerCode',
        'Reference Period Code',
        'Reference Period',
        'Flag Codes',
        'Flags'
        ],
    inplace=True
    )

    df['Subject'] = df['Subject'].map(lambda s: s.strip(' '))
    df['Activity'] = df['Activity'].map(lambda s: s.strip(' '))
    df['Year'].astype(int)
    return df