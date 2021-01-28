"""
This script is the entrypoint to the model docker container for SageMaker. It expects a parameter of either "train" or
"serve" and then triggers the appropriate script.
"""
from argparse import ArgumentParser

from train import run_training
from serve import start_server


if __name__ == '__main__':
    parser = ArgumentParser(description='select model training or serving entrypoint')
    parser.add_argument('entrypoint', choices=['train', 'serve'])
    args = parser.parse_args()
    if args.entrypoint == 'train':
        run_training()
    else:
        start_server()
