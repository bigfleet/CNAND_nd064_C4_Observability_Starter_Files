kind create cluster --config mid.yml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

kubectl create ns monitoring
helm install kind-p -n monitoring prometheus-community/prometheus
helm install kind-g -n monitoring bitnami/grafana

kubectl create ns observability
helm install kind-j -n observability jaegertracing/jaeger \
  --set provisionDataStore.cassandra=false \
  --set allInOne.enabled=true \
  --set storage.type=none \
  --set agent.enabled=false \
  --set collector.enabled=false \
  --set query.enabled=false