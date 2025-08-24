# Recommended Terraform Structure
```
infra/
  network/   # VPC, subnets, networking (almost never changes)
  eks/       # EKS cluster and node groups (rarely changes)
  app/       # Buckets, lambdas, roles, pods, etc. (changes frequently)
```

## How to Use

- Each folder is an independent Terraform project.
- Run `terraform init`, `plan`, `apply` inside the folder you want to modify.
- The recommended order is:
  1. `network/` (first, only once)
  2. `eks/` (after network)
  3. `app/` (may change frequently)

## Variables
- Define your variables in each folder (`terraform.tfvars` or via CLI).
- You can copy your `terraform.tfvars` to each folder or use symlinks.

## Usage Example
```sh
cd infra/network && terraform init && terraform apply
cd ../eks && terraform init && terraform apply
cd ../app && terraform init && terraform apply
```


# How to Start the Cluster Locally
`minikube start`
```
kubectl apply -f k8s/RabbitMQ/rabbitmq-namespace.yaml
kubectl apply -f k8s/RabbitMQ/rabbitmq-statefulset.yaml
kubectl apply -f k8s/RabbitMQ/rabbitmq-service.yaml
kubectl apply -f k8s/RabbitMQ/rabbitmq-deployment.yaml
kubectl get pods -n messaging
kubectl get svc -n messaging
kubectl port-forward svc/rabbitmq 15672:15672 -n messaging
```

# Make File commands

`make test` Execute test sending a image to the API Gateway Endpoint

`build-lambda`Zip the lambda code inside the /app folder so terraform apply on app works.
