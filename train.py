"""
Entrypoint to run the model etl and training pipeline.
"""

import logging
import os
from typing import Callable, Iterable
import traceback

from pipeline.etl import format_source_data, seasonal_difference
from pipeline.model import train_model

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# sagemaker-specific paths
prefix = os.getenv('ROOT_PATH', '/opt/ml')

input_path = os.getenv('SM_INPUT_DIR', os.path.join(prefix, 'input', 'data'))
output_path = os.getenv('SM_OUTPUT_DATA_DIR', os.path.join(prefix, 'output'))
model_path = os.getenv('SM_MODEL_DIR', os.path.join(prefix, 'model'))
param_path = os.getenv('SM_INPUT_CONFIG_DIR', os.path.join(prefix, 'input', 'config'))
# channel name for raw input training data
training_channel = os.getenv('SM_CHANNEL_TRAINING', 'training')
source_data_path = os.path.join(input_path, training_channel)


def execute_pipeline(steps: Iterable[Callable], *args, **kwargs):
    """
    Assemble a pipeline and call each step in sequence.
    :param steps: iterable of pipeline functions
    :param args: arguments passed to the pipeline functions
    :param kwargs: arguments passed to the pipeline functions
    :return:
    """
    for step in steps:
        step(*args, **kwargs)


def run_training():
    """
    Run the pipeline with the data ETL and model training steps, passing in the data source and model save paths.
    :return:
    """
    # TODO: argparse hyparparms
    try:
        execute_pipeline(
            (format_source_data, seasonal_difference, train_model),
            source_path=source_data_path,
            training_data_path=source_data_path,
            model_save_path=model_path,
            season_len=12
        )
    except Exception as e:
        with open(os.path.join(output_path, 'failure'), 'w') as f:
            f.write(f'Exception raised during training\n\n{str(e)}\n{traceback.format_exc()}')
        raise e


if __name__ == '__main__':
    run_training()
