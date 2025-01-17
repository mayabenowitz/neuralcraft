# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from clean import clean_lpc_data, clean_prod_growth_data


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    clean_lpc_data()
    clean_prod_growth_data(
        input_filepath='../data/raw/productivity_growth.csv', 
        output_filepath='../data/processed/productivity_growth.csv'
    )
    clean_prod_growth_data(
        input_filepath='../data/raw/productivity_growth_by_industry.csv',
        output_filepath='../data/processed/productivity_growth_by_industry.csv'
    )
    
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
