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

![Jaeger 500 trace](/answer-img/6-jaeger-trace.png)

#### Cache query results

Date: 2003/04/10

Subject: Trial query introduces high latency with low information change

Affected Area: trial

Severity: Medium

Description:

Consider adding an in-memory cache to avoid repeated requests to an API endpoint, with cache warming as a part of application startup.

The GitHub API request pushes service outside of its latency SLI on the uptime SLO.

### SLIs

Given an SLO commitment of our application has a 99.95% uptime per month, we'd be interested in the following SLIs:

* Measured availability of the service
* Error rate of requests to the service
* Throughput, or total requests to the service
* Latency, or response time for each request to the service

### KPIs

Here, again, is the dashboard.

![Grafana Dashboard Sample](/answer-img/3-grafana-dash.png)

#### Error rates and budgets

*SLI: Less than 1% of requests to service should result in 500 status codes*

Status codes in the 200's and 300's are commonplace in web service software.
Services operating on the public internet are subject to all manner of traffic with malicious intent, much of which will be in the 400 class.  It forms a poor basis for a SLI because it won't go up and down as customer experience improves.
500 errors, on the other hand, are always an issue that the technical team can improve.  A 503 usually indicates a service has failed or is struggling to meet its goals in a fixed timeframe.  A 500 is often a programming error.  These errors are good candidates to track with an SLI, as customer experience can always be improved, and it's a leading indicator.

The graph in the dashboard shows this error rate tracked for each service.  Presenting this together can help determine if there are any correlations in increased error rates that might be even more pressing.

#### Latency

*SLI: At the 95th percentile of latency, requests to service should return in less than 1 second*

Speed is paramount to the customer experience on the Internet.  The curve of satisfaction drops steeply at higher values for response time, while the difference between very fast and fast is not as important.  With this preference set, we want to set an expectation on the basis of the largest preponderance of our responses, while retaining some resistance to having a single outlier move us past a threshold.

Latency is displayed in a table above.    The table contains average, p50, p95 and p99 timings for each service in the time period.

Since the time this course was written, Grafana has iterated on its table concept, and I was not able to completely eliminate or reduce the "time" column without making the response figures inaccurate, so those are still there.

#### Availability

*SLI: Fewer than 1 container restarts for service per 24hr period*

With a Kubernetes runtime, a container restart is a reasonable proxy for momentary unavailability, particularly if our deployments currently target 1 replica, as they do today.

These are raw statistics, and are not graphed.

## Learnings

Jaeger is a service that you run and make operational decisions about.  The all-in-one is like running it on your laptop.  You probably don't want that in prod.

Jaeger operator is like "client discovery" -- client applications can "opt-in" with an inject annotation.  You want to run the operator (with attendant Jaeger crd's and configs) anywhere that can transmit to the Jaeger you've set up.

![Final Grafana Dashboard Sample](/answer-img/5-final-dashboard.png)

Visit it [here](https://www.grafana.tekton.wolf.bigfleet.dev/d/wmVh9hL4z/slo-submissions?orgId=1).

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

