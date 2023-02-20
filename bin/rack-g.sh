echo "Password: $(kubectl get secret kind-g-grafana-admin --namespace monitoring -o jsonpath="{.data.GF_SECURITY_ADMIN_PASSWORD}" | base64 -d)"

kubectl port-forward $(kubectl get pods -l app.kubernetes.io/name=grafana --namespace monitoring --output name) 13000:3000 -n monitoring