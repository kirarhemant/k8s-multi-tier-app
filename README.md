# Kubernetes Multi-Tier Application Deployment

## Project Overview
Deployment of a Flask API with MySQL database on GKE Autopilot, demonstrating:
- Containerization with Docker
- Kubernetes deployments and services
- Persistent storage with PersistentVolumeClaims
- Configuration management using ConfigMaps and Secrets
- High availability for stateful services

## Repository Contents
```bash
k8s-multi-tier-app/
├── app/
│ ├── app.py # Flask application code
│ ├── requirements.txt # Python dependencies
│ └── Dockerfile # API service image build
├── db/
│ ├── init.sql # Database schema
│ └── Dockerfile # MySQL image build
└── k8s/
├── 01-secret.yaml # Database credentials
├── 02-configmap.yaml # Application configuration
├── 03-db-pvc.yaml # Persistent volume claim
├── 04-db-deployment.yaml # Database deployment
├── 05-app-deployment.yaml # API deployment
└── 06-ingress.yaml # Ingress configuration
```

## Deployment Details
- **API Endpoint**: http://34.160.8.119/products
- **Docker Images**:
  - API Service: [`kirarhemant/api-service:v2`](https://hub.docker.com/repository/docker/kirarhemant/api-service/)
  - MySQL DB: [`kirarhemant/mysql-db:v1`](https://hub.docker.com/repository/docker/kirarhemant/mysql-db)
 
## Prerequisites
1. **Google Cloud Account** with:
   - GKE Autopilot cluster created
2. **Local Tools**:
   - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (`gcloud`)
   - [kubectl](https://kubernetes.io/docs/tasks/tools/)
   - [Docker](https://docs.docker.com/get-docker/)

## Setup Instructions
1. Build and push Docker images (or reuse existing images from Docker Hub):
   ```bash
   # API Service
   docker build -t kirarhemant/api-service:v2 ./app
   docker push kirarhemant/api-service:v2

   # MySQL Database
   docker build -t kirarhemant/mysql-db:v1 ./db
   docker push kirarhemant/mysql-db:v1
   ```

2. Deploy to Kubernetes:
   ```bash
   # Apply configurations in order
   kubectl apply -f k8s/01-secret.yaml
   kubectl apply -f k8s/02-configmap.yaml
   kubectl apply -f k8s/03-db-pvc.yaml
   kubectl apply -f k8s/04-db-deployment.yaml
   kubectl apply -f k8s/05-app-deployment.yaml
   kubectl apply -f k8s/06-ingress.yaml
   ```

3. Network Configuration:
   ```bash
   # Creates a firewall rule to allow incoming HTTP traffic
   gcloud compute firewall-rules create allow-http --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0
   ```

4. Health Check Configuration:
   ```bash
   # Since, GCE's default health check was probing port 80 (but app runs on 5000), we have to update made it check port 5000 (Flask app's port - an endpoint that returns HTTP 200). The Ingress controller marks backends as "HEALTHY" only when health checks pass. Once health checks succeed, traffic flows from Ingress to API pods.
   
   # Get health check name
   gcloud compute health-checks list

   # Update health check parameters
   gcloud compute health-checks update http $HEALTH_CHECK --port=5000 --request-path=/products
   ```

## Verification
1. Check Deployment Status
   ```bash
   kubectl get all,ingress,pvc
   ```
2. Test API Endpoint
   ```bash
   # Expected output: JSON list of products
   curl http://34.160.8.119/products
   ```

## Resilience Tests
1. API Pod Regeneration
   ```bash
   # Get list of pods
   kubectl get pods -l app=api
   
   # Delete a pod
   kubectl delete pod $POD_NAME

   # watch regeneration
   kubectl get pods -l app=api --watch
   ```
2. Database Persistence Test
   ```bash
   # Get list of pods
   kubectl get pods -l app=db
   
   # Add test record
   kubectl exec -it $POD_NAME -- mysql -uroot -p$DB_PASSWORD -e "INSERT INTO appdb.products (name) VALUES ('persistence_test');"

   # Delete pod
   kubectl delete pod $POD_NAME

   # watch regeneration
   kubectl get pods -l app=db --watch

   # Get fresh list of pods
   kubectl get pods -l app=db
   
   # Verify data persists
   kubectl exec -it $POD_NAME -- mysql -uroot -p$DB_PASSWORD -e "SELECT * FROM appdb.products WHERE name='persistence_test';"
   ```

## Architecture Notes
API Tier:
1. 4 replicas for high availability
2. Connection pooling to database
3. External access via Ingress

Database Tier:
1. Single replica with persistent storage
2. Automatic recovery with data preservation
3. Internal ClusterIP service
