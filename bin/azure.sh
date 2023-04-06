kubectl create ns ingress-nginx 

helm install ingress-nginx ingress-nginx \
--repo https://kubernetes.github.io/ingress-nginx \
--namespace ingress-nginx \
--set controller.metrics.enabled=true \
--set-string controller.podAnnotations."prometheus\.io/scrape"="true" \
--set-string controller.podAnnotations."prometheus\.io/port"="10254"

kubectl create ns monitoring
helm install kind-p -n monitoring prometheus-community/prometheus
helm install kind-g -n monitoring bitnami/grafana

kubectl apply --kustomize github.com/kubernetes/ingress-nginx/deploy/prometheus/

helm install cert-manager jetstack/cert-manager \
  --set installCRDs=true \
  --set podLabels.aadpodidbinding="certman-label"

kubectl create ns observability

helm install -n observability kind-j jaegertracing/jaeger-operator \
  -f j-args.yml

kubectl create -f https://download.elastic.co/downloads/eck/2.6.1/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.6.1/operator.yaml
