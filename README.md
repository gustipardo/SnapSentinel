# Estructura recomendada de Terraform

```
infra/
  network/   # VPC, subnets, networking (casi nunca cambia)
  eks/       # EKS cluster y node groups (cambia poco)
  app/       # Buckets, lambdas, roles, pods, etc. (cambia seguido)
```

## Cómo usar

- Cada carpeta es un proyecto Terraform independiente.
- Ejecuta `terraform init`, `plan`, `apply` dentro de la carpeta que quieras modificar.
- El orden recomendado es:
  1. `network/` (primero, una sola vez)
  2. `eks/` (después de network)
  3. `app/` (puede cambiar seguido)

## Variables
- Define tus variables en cada carpeta (`terraform.tfvars` o por CLI).
- Puedes copiar tu `terraform.tfvars` a cada carpeta o usar symlinks.

## Ejemplo de uso
```sh
cd infra/network && terraform init && terraform apply
cd ../eks && terraform init && terraform apply
cd ../app && terraform init && terraform apply
```


# Como iniciar el cluster de forma local
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