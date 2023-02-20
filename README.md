## Cloud Native Architecture Nanodegree (CNAND): Observability

This is the public repository for the Observability course of Udacity's Cloud Native Architecture Nanodegree (CNAND) program (ND064).

The  **Exercise_Starter_Files** directory has all of the files you'll need for the exercises found throughout the course.

The **Project_Starter_Files** directory has the files you'll need for the project at the end of the course.

## Lurnings

Jaeger is a service that you run and make operational decisions about.  The all-in-one is like running it on your laptop.  You probably don't want that in prod.

Jaeger operator is like "client discovery" -- client applications can "opt-in" with an inject annotation.  You want to run the operator (with attendant Jaeger crd's and configs) anywhere that can transmit to the Jaeger you've set up.

## My notes



When configuring Grafana sources:

Prometheus is the "server" service on Port 80 (9090 is container port)
Jaeger is the query service on port 16686

http://kind-p-prometheus-server.monitoring.svc.cluster.local
http://simpletest-query.default.svc.cluster.local:16686

Cluster DNS works in both instances

### Grafana-ing

container_threads
node_memory_MemTotal_bytes
node_cpu_seconds_total

###

kubectl port-forward $(kubectl get pods -l app=prometheus --namespace monitoring --output name) 9090:9090 -n monitoring

kubectl port-forward $(kubectl get pods -l app.kubernetes.io/name=grafana --namespace monitoring --output name) 13000:3000 -n monitoring

kubectl port-forward $(kubectl get pods -l app=hello --namespace default --output name) 18080:8080 -n default

kubectl port-forward $(kubectl get pods -l app.kubernetes.io/name=simpletest --namespace default --output name) 16686:16686 -n default
