"""
Adapted from https://github.com/aws/amazon-sagemaker-examples/tree/master/advanced_functionality/scikit_bring_your_own
This is a wrapper for gunicorn to find the flask app
"""

import inference_handler as myapp

app = myapp.app
