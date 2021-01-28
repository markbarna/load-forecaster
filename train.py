"""
Entrypoint to run the model etl and training pipeline.
"""

import logging
import os
from typing import Callable, Iterable
import traceback

from pipeline.etl import format_source_data
from pipeline.model import train_model

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# sagemaker-specific paths
prefix = os.getenv('ROOT_PATH', '/opt/ml')

# TODO: Update to ENV vars
input_path = os.path.join(prefix, 'input', 'data')
output_path = os.path.join(prefix, 'output')
model_path = os.path.join(prefix, 'model')
param_path = os.path.join(prefix, 'input/config/hyperparameters.json')
# channel name for raw input training data
channel_name = 'training'
source_data_path = os.path.join(input_path, channel_name)


def execute_pipeline(steps: Iterable[Callable], *args, **kwargs):
    for step in steps:
        step(*args, **kwargs)


def run_training():
    # TODO: argparse hyparparms
    try:
        execute_pipeline(
            (format_source_data, train_model),
            source_path=source_data_path,
            training_data_path=source_data_path,
            model_save_path=model_path
        )
    except Exception as e:
        with open(os.path.join(output_path, 'failure'), 'w') as f:
            f.write(f'Exception raised during training\n\n{str(e)}\n{traceback.format_exc()}')
        raise e


if __name__ == '__main__':
    run_training()
