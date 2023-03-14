kubectl apply -f Project_Starter_Files-Building_a_Metrics_Dashboard/manifests/other/elasticsearch.yaml

sleep 20

kubectl wait --namespace default \
  --for=condition=ready pod \
  --selector=statefulset.kubernetes.io/pod-name=quickstart-es-default-0 \
  --timeout=90s

ES_PASSWORD=$(kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}')

kubectl create secret generic jaeger-secret --from-literal=ES_PASSWORD=$ES_PASSWORD --from-literal=ES_USERNAME=elastic

kubectl apply -f Project_Starter_Files-Building_a_Metrics_Dashboard/manifests/other/jaeger-elasticsearch.yaml

sleep 20

kubectl wait --namespace default \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/name=simple-prod-collector \
  --timeout=90s

helm install community-operator mongodb/community-operator

kubectl apply -f Project_Starter_Files-Building_a_Metrics_Dashboard/manifests/other/mongo.yaml

sleep 20

kubectl wait --namespace default \
  --for=condition=ready pod \
  --selector=statefulset.kubernetes.io/pod-name=example-mongodb-0 \
  --timeout=90s

kubectl apply -f Project_Starter_Files-Building_a_Metrics_Dashboard/manifests/app/backend.yaml
kubectl apply -f Project_Starter_Files-Building_a_Metrics_Dashboard/manifests/app/frontend.yaml
kubectl apply -f Project_Starter_Files-Building_a_Metrics_Dashboard/manifests/app/mongoc.yaml
kubectl apply -f Project_Starter_Files-Building_a_Metrics_Dashboard/manifests/app/trial.yaml