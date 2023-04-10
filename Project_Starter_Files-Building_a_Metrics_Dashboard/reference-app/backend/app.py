import logging
import os

from flask import Flask, render_template, request, jsonify
from flask_opentracing import FlaskTracing
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_flask_exporter import PrometheusMetrics

import pymongo
from flask_pymongo import PyMongo

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

metrics = PrometheusMetrics(app)
# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")

logging.getLogger("").handlers = []
logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_tracer(service):

    config = Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "logging": True,
            "reporter_batch_size": 1,
        },
        service_name=service,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(service_name_label=service),
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


tracer = init_tracer("backend")
flask_tracer = FlaskTracing(tracer, True, app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)


@app.route("/")
def homepage():
    return "Hello World"


@app.route("/api")
def my_api():
    with tracer.start_span("backend-api") as span:
      answer = "something"
      return jsonify(repsonse=answer)

@app.route("/star", methods=["GET"])
def star():
    with tracer.start_span("get-star") as span:
      star = mongo.db.stars
      new_star = star.find_one_or_404()
      return jsonify({"result": new_star})

@app.route("/star", methods=["POST"])
def add_star():
    with tracer.start_span("post-star") as span:
      star = mongo.db.stars
      name = request.json["name"]
      distance = request.json["distance"]
      star_id = star.insert({"name": name, "distance": distance})
      new_star = star.find_one({"_id": star_id})
      output = {"name": new_star["name"], "distance": new_star["distance"]}
      return jsonify({"result": output})

if __name__ == "__main__":
    app.run()
