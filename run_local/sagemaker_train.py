from sagemaker.estimator import Estimator
from argparse import ArgumentParser

if __name__ == '__main__':
    """
    usage: sagemaker_train.py [-h] [-t TRAINING] [-o OUTPUT] [-e {local,S3}] [-r ROLE] image_uri

    Train load forecaster using Sagemaker
    
    positional arguments:
      image_uri             URI of the docker image
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TRAINING, --training TRAINING
                            training data directory
      -o OUTPUT, --output OUTPUT
                            output path directory
      -e {local,S3}, --environment {local,S3}
                            run image locally (requires docker) (default) or in S3
      -r ROLE, --role ROLE  AWS role ARN
    """
    arg_parser = ArgumentParser(description='Train load forecaster using Sagemaker')
    arg_parser.add_argument('image_uri', help='URI of the docker image')
    arg_parser.add_argument('-t', '--training', default='training', help='training data directory'),
    arg_parser.add_argument('-o', '--output', default='', help='output path directory')
    arg_parser.add_argument(
        '-e', '--environment', default='local', choices=['local', 'S3'],
        help='run image locally (requires docker) (default) or in S3'
    )
    arg_parser.add_argument(
        '-r', '--role', default='arn:aws:iam::111122223333:role/role-name', help='AWS role ARN'
    )
    args = arg_parser.parse_args()
    instance_type = 'local'
    path_uri = 'file'
    if args.environment == 'S3':
        instance_type = ''
        path_uri = 'S3'
    out_path = path_uri + '://' + args.output
    train_path = path_uri + '://' + args.training

    estimator = Estimator(
        image_uri=args.image_uri,
        role=args.role,
        instance_count=1,
        instance_type=instance_type,
        output_path=out_path
    )
    estimator.fit(train_path)
