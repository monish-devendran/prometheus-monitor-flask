import logging
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Configure request logging
request_logger = logging.getLogger('werkzeug')
request_logger.setLevel(logging.INFO)
app.logger.addHandler(logging.StreamHandler())

@app.before_request
def log_request_info():
    app.logger.info('Request: %s %s', request.method, request.url)

@app.route('/')
def hello_world():
    return 'Hello, Kubernetes! with prometheus configured with logging';

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
