import logging
import os
from typing import Callable, Iterable

from pipeline.etl import format_source_data
from pipeline.model import train
from utils.utils import PROJECT_ROOT

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def execute_pipeline(steps: Iterable[Callable], *args, **kwargs):
    for step in steps:
        step(*args, **kwargs)


if __name__ == '__main__':
    execute_pipeline(
        (format_source_data, train),
        source_path=os.path.join(PROJECT_ROOT, 'data', 'source'),
        training_data_path=os.path.join(PROJECT_ROOT, 'data', 'transformed'),
        model_save_path=os.path.join(PROJECT_ROOT, 'data', 'output')
    )
