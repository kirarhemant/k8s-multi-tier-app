# Kubernetes Multi-Tier Application Deployment

## Project Overview
Deployment of a Flask API with MySQL database on GKE Autopilot, demonstrating:
- Containerization
- Kubernetes deployments
- Persistent storage
- Configuration management

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

text

## Deployment Details
- **API Endpoint**: http://34.160.8.119//products
- **Docker Images**:
  - API Service: `kirarhemant/api-service:v2`
  - MySQL DB: `kirarhemant/mysql-db:v1`

## Setup Instructions
1. Build and push Docker images:
   ```bash
   docker build -t kirarhemant/api-service:v2 ./app
   docker push kirarhemant/api-service:v2
   
   docker build -t kirarhemant/mysql-db:v1 ./db
   docker push kirarhemant/mysql-db:v1
   ```

2. Deploy to Kubernetes:
   ```bash
   kubectl apply -f k8s/01-secret.yaml
   kubectl apply -f k8s/02-configmap.yaml
   kubectl apply -f k8s/03-db-pvc.yaml
   kubectl apply -f k8s/04-db-deployment.yaml
   kubectl apply -f k8s/05-app-deployment.yaml
   kubectl apply -f k8s/06-ingress.yaml
   ```
