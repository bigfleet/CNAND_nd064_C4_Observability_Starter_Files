import logging
import re
import requests
import os


from flask import Flask, jsonify, render_template
from flask_opentracing import FlaskTracing
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_flask_exporter import PrometheusMetrics

gh_token = os.getenv("GITHUB_TOKEN")

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


tracer = init_tracer("trial")
flask_tracer = FlaskTracing(tracer, True, app)


@app.route("/")
def homepage():
    return render_template("main.html")


@app.route("/trace")
def trace():
    def remove_tags(text):
        tag = re.compile(r"<[^>]+>")
        return tag.sub("", text)

    with tracer.start_span("get-python-repos") as span:
        url = "https://api.github.com/search/repositories?q=python"
        headers= {
              'Accept': 'application/vnd.github+json',
              'Authorization': f"Bearer {gh_token}",
              'X-GitHub-Api-Version': '2022-11-28'
        }
        res = requests.get(url, headers=headers)
        span.log_kv({"event": "get repos count", "count": len(res.json())})
        span.set_tag("repos-count", len(res.json()))
        repos_info = []
        for result in res.json()['items']:
            #logger.debug(f"result {result}")
            repos = {}
            with tracer.start_span("request-site") as site_span:
                logger.info(f"Getting result for {result}")
                logger.info(f"Getting website for {result['full_name']}")
                try:
                    repos["full_name"] = remove_tags(result["full_name"])
                    repos["description"] = result["description"]
                    repos["owner"] = result["owner"]["login"]
                    repos["owner_url"] = result["owner"]["url"]
                    repos["owner_type"] = result["owner"]["type"]
                    repos["name"] = result["name"]
                    repos["type"] = result["language"]
                    repos["url"] = result["html_url"]

                    repos_info.append(repos)
                    site_span.set_tag("http.status_code", res.status_code)
                    site_span.set_tag("company-site", result["html_url"])
                except Exception:
                    logger.error(f"Unable to get site for {result['company']}")
                    site_span.set_tag("http.status_code", res.status_code)
                    site_span.set_tag("company-site", result["html_url"])

    return jsonify(repos_info)


if __name__ == "__main__":
    app.run(debug=True,)
