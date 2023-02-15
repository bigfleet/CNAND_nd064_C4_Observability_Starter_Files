import os
import time
import requests

from flask import Flask, jsonify

import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracer

import redis
#import redis_opentracing

app = Flask(__name__)

rdb = redis.Redis(host="redis-primary.default.svc.cluster.local", port=6379, db=0)


def init_tracer(service):
    logging.getLogger("").handlers = []
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)

    config = Config(
      config={
        'sampler':
          {
            'type': 'const', 'param': 1
          },
          'logging': True,
          'reporter_batch_size': 1,
      }, 
      service_name="service")

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

tracer = init_tracer("test-service")

# not entirely sure but I believe there's a flask_opentracing.init_tracing() missing here
flask_tracer = FlaskTracer(tracer, True, app)
#redis_opentracing.init_tracing(tracer, trace_all_classes=False)

with tracer.start_span("first-span") as span:
    span.set_tag("first-tag", "100")


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/alpha")
def alpha():
    with tracer.start_span("alpha") as span:
      for i in range(100):
          with tracer.start_span('alpha-heavy', child_of=span) as child_span:
            if i % 100 == 99:
                time.sleep(10)
      return "This is the Alpha Endpoint!"


@app.route("/beta")
def beta():
    with tracer.start_span("beta") as span:
      r = requests.get("https://www.google.com/search?q=python")
      dict = {}
      for key, value in r.headers.items():
        print(key, ":", value)
        dict.update({key: value})
      return jsonify(dict)


@app.route(
    "/writeredis"
)  # needed to rename this view to avoid function name collision with redis import
def writeredis():
    # start tracing the redis client
    #redis_opentracing.trace_client(rdb)
    r = requests.get("https://www.google.com/search?q=python")
    dict = {}
    # put the first 50 results into dict
    for key, value in r.headers.items()[:50]:
        print(key, ":", value)
        dict.update({key: value})
    rdb.mset(dict)
    return jsonify(dict)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
