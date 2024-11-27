#!/bin/bash

# Define the Kubernetes directory (adjust the path as needed)
K8S_DIR="./k8s"

# Check if the directory exists
if [ ! -d "$K8S_DIR" ]; then
  echo "Directory $K8S_DIR does not exist!"
  exit 1
fi

# Apply all YAML files in the k8s directory
echo "Applying all YAML files in the $K8S_DIR directory..."

kubectl apply -f $K8S_DIR/

# Check if the apply was successful
if [ $? -eq 0 ]; then
  echo "Kubernetes resources successfully applied."
else
  echo "There was an error applying the Kubernetes resources."
  exit 1
fi
