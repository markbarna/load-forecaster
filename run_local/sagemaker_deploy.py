"""
Deploy the trained model using SageMaker.
"""

from sagemaker.model import Model
from sagemaker.predictor import Predictor
from sagemaker.deserializers import StringDeserializer
from sagemaker.serializers import JSONSerializer
from argparse import ArgumentParser


class ModelPredictor(Predictor):

    def __init__(self, endpoint_name: str, sagemaker_session=None):
        super().__init__(
            endpoint_name=endpoint_name,
            sagemaker_session=sagemaker_session,
            deserializer=StringDeserializer(),
            serializer=JSONSerializer()
        )


if __name__ == '__main__':
    """
    usage: sagemaker_deploy.py [-h] [-o OUTPUT] [-e {local,S3}] [-r ROLE] image_uri
    
    Deploy load forecaster using Sagemaker
    
    positional arguments:
      image_uri             URI of the docker image
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            output path directory
      -e {local,S3}, --environment {local,S3}
                            run image locally (requires docker) (default) or in S3
      -r ROLE, --role ROLE  AWS role ARN
    """
    arg_parser = ArgumentParser(description='Deploy load forecaster using Sagemaker')
    arg_parser.add_argument('image_uri', help='URI of the docker image')
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

    model = Model(
        image_uri=args.image_uri,
        model_data=f'{out_path}model.tar.gz',
        role=args.role,
        predictor_cls=ModelPredictor
    )

    model.deploy(initial_instance_count=1, instance_type='local', endpoint_name='load-forecaster')
