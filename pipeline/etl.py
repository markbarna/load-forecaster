import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)


def format_source_data(source_path: str, *args, **kwargs):
    """
    Load the load source csv files, join them, sort, and encode data fields
    :param source_path:
    :return:
    """
    # load and join tables
    logger.info(f"====== Loading raw data from {source_path} ======")
    df = pd.concat((pd.read_csv(file.path)) for file in os.scandir(source_path) if file.name.endswith('.csv'))

    # drop unused fields, encode data types
    df = df[['datetime_beginning_utc', 'area', 'instantaneous_load']]
    df = df.rename(columns={'datetime_beginning_utc': 'datetime', 'instantaneous_load': 'load'})
    # TODO: reduce to second resolution
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['area'] = df['area'].astype('category')

    # sort by UTC date and time
    df = df.sort_values('datetime')
    df = df.set_index('datetime')

    # order columns so variable load data is first and categorical area variable is second
    df = df[['load', 'area']]

    df.to_parquet(os.path.join(source_path, 'training_data.parquet'), index=True)
    logger.info(f"====== ETL complete on {len(df)} samples "
                f"from {df.index.min()} to {df.index.max()} ======")
