import joblib
import flask
from werkzeug.exceptions import BadRequest
import logging

from pipeline.model import TimeSeriesModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class HandlerService:
    model: TimeSeriesModel = None

    @classmethod
    def get_model(cls):
        if cls.model is None:
            # TODO: Make model path a variable
            cls.model = joblib.load('/opt/ml/model/model.gz')
        return cls.model

    @classmethod
    def predict(cls, *args, **kwargs):
        return cls.model.predict(*args, **kwargs)


# The flask app for serving predictions
app = flask.Flask(__name__)


@app.before_first_request
def load_model():
    HandlerService.get_model()


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = HandlerService.get_model() is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    logger.info(f'content type received: {flask.request.content_type}')
    try:
        request_data = flask.request.get_json()
    except BadRequest as e:
        error_msg = f'Bad request: {e}'
        logger.error(error_msg)
        return flask.Response(response=error_msg, status=400, mimetype='text/plain')
    if request_data is None:
        return flask.Response(
            response='This predictor only supports application/json data.', status=415, mimetype='text/plain'
        )

    logger.info(f'Input received: {request_data}.')

    try:
        # return value is a single-element Series, which needs to be converted into a string for the response
        prediction = HandlerService.predict(**request_data)
    except TypeError as e:
        error_msg = f'Error, bad request data decoded. Prediction failed due to: {e}'
        logger.error(error_msg)
        return flask.Response(response=error_msg, status=400, mimetype='text/plain')
    logger.info(f'Prediction:\n{prediction}')
    response_value = f"{prediction.iloc[0]:.2f} MW"

    return flask.Response(response=response_value, status=200, mimetype='text/plain')
