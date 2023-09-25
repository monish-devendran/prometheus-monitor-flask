import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, Response, jsonify
from time import strftime
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, generate_latest, CollectorRegistry
import traceback


app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Configure request logging
request_logger = logging.getLogger('werkzeug')
request_logger.setLevel(logging.INFO)
app.logger.addHandler(logging.StreamHandler())

registry = CollectorRegistry()
custom_metric = Counter('flask_custom_metric', 'Description of custom metric', registry=registry)


@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

# @app.errorhandler(Exception)
# def exceptions(e):
#     tb = traceback.format_exc()
#     print(e)
#     timestamp = strftime('[%Y-%b-%d %H:%M]')
#     logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
#     return e.status_code


@app.route("/json")
def get_json():
    data = {"Name":"Ivan Leon","Age":"27","Books":"[Crime and Punishment, The Gambler, Twenty Thousand Leagues Under The Sea]"}
    return jsonify(data_WRONG) # INTENTIONAL ERROR FOR TRACEBACK EVENT

@app.route('/')
def hello_world():
    return 'Hello, Kubernetes! with prometheus configured with logging';

@app.route('/custom_metrics')
def metrics():
    return Response(generate_latest(registry), mimetype='text/plain')

@app.route('/increment')
def increment_metric():
    custom_metric.inc()
    return 'Custom metric incremented'


if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    logger = logging.getLogger('tdm')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    app.run(host='0.0.0.0', port=5000)
