# MicroK8s Scalable Microservices Project

A cloud-native, auto-scaling microservices architecture deployed locally using MicroK8s. This project demonstrates containerized deployment, a local private registry workflow, dynamic Horizontal Pod Autoscaling (HPA), and ingress routing.

---

## 👥 Team Members
* **吳得豐** (412855180)
* **林大偉** (412855263)
* **高曼柯** (412855289)
* **陳明義** (412855339)

---

## Prerequisites

Ensure your environment meets these hardware and software specifications before starting:
* **OS:** Ubuntu 20.04+ (Virtual Machine or bare-metal)
* **Hardware:** Minimum 4GB RAM, 2 CPU cores
* **Runtimes:** MicroK8s and Docker (Installation steps provided below)

---

## 📂 Architecture & Directory Structure

```text
microk8-shark-main/
│
├── app.py                  # Flask application source code
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container build instructions
│
├── k8s/                    # Kubernetes Manifests
│   ├── deployment.yaml     # App deployment configuration
│   ├── service.yaml        # Internal ClusterIP service
│   ├── ingress.yaml        # NGINX Ingress routing rules
│   └── hpa.yaml            # Horizontal Pod Autoscaler configuration
│
├── static/                 # Resources used in the webpage
│   ├── honk.mp3            # Sound effect for webpage
│   └── logo.jpg            # Image of a shark
│
├── templates/              # The webpage
│   └── index.html          
│
├── README.md               # Installation guide
└── REPORT.pdf              # Final project report

```

---

## ⚙️ Resource Optimization per Pod
​Our deployment manifests are fine-tuned for high density and efficient local resource consumption:
* **​RAM:** 128Mi request / 256Mi limit
* **CPU:** 100m request / 200m limit

---

## Tutorial & Deployment Step

### 1. Clone Repository
```bash
git clone https://github.com/dr2dp/microk8s-shark.git
cd microk8-shark-main
```
---

### 2. Setup Environment
Run these commands to install MicroK8s, configure user permissions, and spin up Docker.

```bash
# Install MicroK8s via Snap
sudo snap install microk8s --classic

# Add your user to the microk8s group and configure local kube directories
sudo usermod -a -G microk8s $USER
mkdir -p ~/.kube
sudo chown -R $USER ~/.kube
newgrp microk8s

# Verify MicroK8s installation status
microk8s status --wait-ready

# Enable required MicroK8s core add-ons
microk8s enable dns
microk8s enable registry
microk8s enable ingress
microk8s enable metrics-server

# Install and configure the Docker engine
sudo apt update
sudo apt install docker.io -y
sudo usermod -aG docker $USER
newgrp docker

```
---

### 3. Build and Push to Local Registry

```bash
# Build the local Docker image
docker build -t my-flask-app:v1 .

# Tag the image targeting the built-in MicroK8s registry (port 32000)
docker tag my-flask-app:v1 localhost:32000/my-flask-app:v1

# Push the tagged image into the local registry
docker push localhost:32000/my-flask-app:v1

# Verify the image is successfully hosted in the private catalog
curl http://localhost:32000/v2/_catalog

```

---


### 4. Deploy Everything
```bash
# Apply all core manifests from the directory
microk8s kubectl apply -f k8s/

# Verify resource deployment status across components
microk8s kubectl get pods
microk8s kubectl get svc
microk8s kubectl get ingress
microk8s kubectl get hpa

# Append a local DNS host entry to match your Ingress rules
echo "127.0.0.1 flask-app.local" | sudo tee -a /etc/hosts

# Wait until the target pods pass health checks
microk8s kubectl wait --for=condition=ready pod -l app=flask-app --timeout=60s

# Test cluster ingress responsiveness
curl http://flask-app.local/info

```
---


### Extra - How to show the webpage
```bash
# Enable MetalLB with an IP range
microk8s enable metallb:10.64.140.43-10.64.140.49

# Find flask-app-service Cluster-IP
microk8s kubectl get svc 

# SSH to tunnel to your machine (do this outside the vm)
ssh -L 8080:$FLASK_APP_SERVICE_IP:80 $VM_USER@localhost -p 8822
# Example:ssh -L 8080:10.152.183.44:80 dr2dp@localhost -p 8822

# Access Through a Web Browser
http://flask-app.local:8080/

```

---
