# kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.11.0/cert-manager.crds.yaml

# kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.41.1/jaeger-operator.yaml -n observability

# kubectl create namespace observability 
# helm install -n observability kind-j jaegertracing/jaeger-operator

# kubectl apply -f https://raw.githubusercontent.com/jaegertracing/helm-charts/main/charts/jaeger-operator/crds/crd.yaml

kubectl apply -f deployment/
