kind create cluster --config mid.yml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
#kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/8045cd29fbaaf720dea7586e5b559005250f03c9/deploy/static/provider/kind/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

kubectl create ns monitoring
helm install kind-p -n monitoring prometheus-community/prometheus
helm install kind-g -n monitoring bitnami/grafana

helm install cert-manager jetstack/cert-manager \
  --set installCRDs=true
        podLabels:
        aadpodidbinding: "certman-label"

kubectl create ns observability

# Jaeger runs but doesn't appear to webhook interact (duh)

# helm install kind-j -n observability jaegertracing/jaeger \
#   --set provisionDataStore.cassandra=false \
#   --set allInOne.enabled=true \
#   --set storage.type=none \
#   --set agent.enabled=false \
#   --set collector.enabled=false \
#   --set query.enabled=false

helm install -n observability kind-j jaegertracing/jaeger-operator \
  -f j-args.yml

kubectl create -f https://download.elastic.co/downloads/eck/2.6.1/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.6.1/operator.yaml


