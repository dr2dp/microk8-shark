# MicroK8s Scalable Microservices Project

## Team Members
- 吳得豐 412855180

## Prerequisites
- Ubuntu 20.04+ (VM or bare metal)
- Minimum 4GB RAM, 2 CPU cores
- MicroK8s installed
- Docker installed

## Tutorial
### 1. Clone Repository
\`\`\`bash
git clone <repo-url>
cd cloud-native
\`\`\`

### 2. Setup Environment
\`\`\`bash
# Install MicroK8s
sudo snap install microk8s --classic

# Add your user to microk8s group
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
newgrp microk8s

# Verify installation
microk8s status --wait-ready

# Enable required addons
microk8s enable dns
microk8s enable registry
microk8s enable ingress
microk8s enable metrics-server

# Install Docker
\`\`\`
sudo apt update
sudo apt install docker.io -y
sudo usermod -aG docker $USER
newgrp docker
\`\`\`

### 3. Build and Push to Local Registry
\`\`\`bash
# Build the image
docker build -t my-flask-app:v1 .

# Tag for local registry
docker tag my-flask-app:v1 localhost:32000/my-flask-app:v1

# Push to MicroK8s registry
docker push localhost:32000/my-flask-app:v1

# Verify image is in registry
curl http://localhost:32000/v2/_catalog
\`\`\`

### 4. Deploy Everything
# Apply all manifests
microk8s kubectl apply -f k8s/

# Verify deployment
microk8s kubectl get pods
microk8s kubectl get svc
microk8s kubectl get ingress
microk8s kubectl get hpa

# Add host entry for testing
echo "127.0.0.1 flask-app.local" | sudo tee -a /etc/hosts

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=flask-app --timeout=60s

# Test the service
curl http://flask-app.local/

## Architecture
cloud-native/
│
├── app.py
├── requirements.txt
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
│
├── Dockerfile
├── traffic.sh
│
├── README.md
├── REPORT.pdf

## Testing
# 1. Registry proof

# List images in registry
curl http://localhost:32000/v2/_catalog

# Show the Dockerfile that builds this image
cat Dockerfile

# Show the K8s manifest pointing to this local registry
cat k8s/deployment.yaml | grep "image:"

# 2. Traffic
chmod +x $traffic.sh
./traffic.sh

# 3. Chaos Test
# Delete a pod
microk8s kubectl delete pod $PODNAME

# Verify service still works
curl http://flask-app.local/

# 4. Scaling Test
microk8s kubectl get pods
microk8s kubectl scale deployment flask-app --replicas=5
microk8s kubectl get pods

NOTE: Containers may self terminate if the hpa was not given enough time to get metrics


# Verify it is recreated
microk8s kubectl get pods -l app=flask-app -w

# Verify service still works
curl http://flask-app.local/

## Resource Constraints
Our deployment is optimized for:
- RAM: 128Mi request, 256Mi limit per pod
- CPU: 100m request, 200m limit per pod
