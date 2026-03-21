# Kubernetes - Minikube Flask Deployment

Przykład z Szkolenia 2: Kubernetes - Praktyka z Minikube i Helm.

## Wymagania

- Minikube (`brew install minikube` / `choco install minikube`)
- kubectl (`brew install kubectl`)

## Uruchomienie

### 1. Start klastra Minikube

```bash
minikube start
minikube status
kubectl get nodes
```

### 2. Build obrazu Docker w kontekscie Minikube

```bash
eval $(minikube docker-env)
docker build -t flask-k8s-demo:1.0 .
```

### 3. Deploy aplikacji

```bash
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl get pods
kubectl get services
```

### 4. Dostep do aplikacji

```bash
minikube service flask-demo-service
# lub
minikube service flask-demo-service --url
```

### 5. Test load balancingu

```bash
for i in {1..6}; do curl $(minikube service flask-demo-service --url); echo; done
```

### 6. Test self-healingu

```bash
kubectl delete pod <nazwa-poda>
kubectl get pods
```

## Produkcyjne manifesty (katalog k8s/)

Pelny zestaw manifestow YAML dla produkcyjnej aplikacji Python:

```bash
kubectl apply -f k8s/
kubectl get all -n my-python-app
```

Zawiera: Namespace, ConfigMap, Secret, Deployment (z probes i resource limits), Service.
