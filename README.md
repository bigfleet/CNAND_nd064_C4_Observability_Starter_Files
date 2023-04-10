## Cloud Native Architecture Nanodegree (CNAND): Observability

This is Jim Van Fleet (@bigfleet)'s copy of the public repository for the Observability course of Udacity's Cloud Native Architecture Nanodegree (CNAND) program (ND064).

## Submission

### Pods

![Pod listing of relevant namespaces.](/answer-img/1-pod-list.svg)

### Prometheus, Jaeger, and Grafana

I completed almost the entire class on an M1 Mac, mostly down to my stubbornness and lack of access to other equipment.  I got almost all the way there with `podman` and `kind`, but this final assignment set proved too much to handle for my laptop with that virtualization scheme at this writing.

As a result, [my cluster](https://www.grafana.tekton.wolf.bigfleet.dev/dashboards) is up on Azure and you can find the `admin` password in my submission.

In the event you want to interact with the front-end and see your own requests reflected live, that is [here](https://nanodegree.tekton.wolf.bigfleet.dev/)

The requested screenshot for submission is this one:

![Grafana Dashboards](/answer-img/2-grafana-home.png)

### Describe SLO/SLI

```
Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.
```

A Service Level Objective (SLO) is a quantifiable, measurable way to verify a commitment is met.  (This commitment itself is often a service level agreement, or SLA.)

A Service Level Indicator is a value (commonly a function of values) that determine whether an SLO has been met, where values are sensor readings or represent facts about the world.

For _monthly uptime_, for example, one relevant measurement is _total number of minutes in April 2023_, which is a calculation, not a sensor reading.  To smooth over calendar irregularities, we may use a "trailing 30 day window," for example.

It would be paired with _total number of uptime minutes in a trailing 30 days period_ for a service to calculate monthly uptime percentage.

For _request response time_, we note this SLO is a commitment regarding latency.  We would want to define _acceptable response time_, (for this example, we'll use 500ms).

We'd want to measure _total requests per period_, as well as _number of requests per period above acceptable response time_.  It's also common for this sort of metric to be captured on percentage bases.  For example "How much time would I need to allot to ensure I'd have my response in 99% of the trials?"

### Creating SLI metrics

For _uptime_, we may want to capture the following:

* *Availability percentage*: This tells us how often our service was available to perform as expected.
* *Error rate*: For applications with uneven usage patterns, or are affected by bugs or faulty deployments, error rate may be a more accurate way to measure how often a service was able to behave correctly.

For _request response time_, we may want to capture the following:

* *Average, p95 and p99 latencies*: This will give us a good sense of the ranges of common experience, safe expectation, and peak response times.

* *Success rates*: This will give us an idea of how many requests for service are typically successful, along with their ranges.  When viewed over time, troughs can be alerted when they occur.

![Grafana Dashboard Sample](/answer-img/3-grafana-dash.png)

### Traces

The [tracing python sample](Project_Starter_Files-Building_a_Metrics_Dashboard/reference-app/trial/app.py) is here in the repository.
The [backend python sample](Project_Starter_Files-Building_a_Metrics_Dashboard/reference-app/backend/app.py) is also here in the repository.

One of the submitted dashboards allows to click on traces from the backend and the trial application.

![Jaeger trace](/answer-img/4-jaeger-trace.png)

### Trouble Tickets

#### Favico

Date: 2003/04/10

Subject: Front-end missing /favicon.ico

Affected Area: frontend

Severity: Low

Description: No favicon.ico packaged with front-end app, browsers request it by default and receive 404.

#### Mongo DB structure

Date: 2003/04/10

Subject: Back-end MongoDB structure not established

Affected Area: backend

Severity: High

Description:

Database interactivity creates 500s

As seen in [this trace](https://www.grafana.tekton.wolf.bigfleet.dev/explore?left=%7B%22datasource%22:%22XJyML2LVk%22,%22queries%22:%5B%7B%22query%22:%226a872069cb5ed0f4%22,%22refId%22:%22A%22%7D%5D,%22range%22:%7B%22from%22:%22now-1h%22,%22to%22:%22now%22%7D%7D&orgId=1&right=%7B%22datasource%22:%22XJyML2LVk%22,%22queries%22:%5B%7B%22query%22:%226a872069cb5ed0f4%22,%22refId%22:%22A%22%7D%5D,%22range%22:%7B%22from%22:%221681136032465%22,%22to%22:%221681139632465%22%7D,%22panelsState%22:%7B%22trace%22:%7B%22spanId%22:%2263b680da6e445b07%22%7D%7D%7D), the MongoDB created for this application still has insufficient structure to respond correctly with respect to forming a response on the server-side.  Either interact with the created database in a way to resolve this issue, improve your error handling, or provide operations with a database preparation script that we can ensure runs as a part of service start-up.

## Learnings

Jaeger is a service that you run and make operational decisions about.  The all-in-one is like running it on your laptop.  You probably don't want that in prod.

Jaeger operator is like "client discovery" -- client applications can "opt-in" with an inject annotation.  You want to run the operator (with attendant Jaeger crd's and configs) anywhere that can transmit to the Jaeger you've set up.

## My (local) notes

When configuring Grafana sources:

Prometheus is the "server" service on Port 80 (9090 is container port)
Jaeger is the query service on port 16686

http://kind-p-prometheus-server.monitoring.svc.cluster.local
http://prometheus-server.ingress-nginx.svc.cluster.local
http://simpletest-query.default.svc.cluster.local:16686
http://simple-prod-query.default.svc.cluster.local:16686
http://prometheus-server.ingress-nginx.svc.cluster.local:9090
http://simple-prod-query.default.svc:16686

Cluster DNS works in both instances

