# Makefile para SnapSentinel

.PHONY: test build-lambda


# 0_ingest

## terraform apply para la etapa 1_ingest
tf-apply-1_ingest: build-lambda-snapshot_ingestor
	cd terraform/stages/1_ingest && terraform apply -var-file="terraform.dev.tfvars"

## terraform destroy para la etapa 1_ingest
tf-destroy-1_ingest:
	cd terraform/stages/1_ingest && terraform destroy -var-file="terraform.dev.tfvars" -auto-approve


## test envia una imagen a la API Gateway, Lambda la sube a S3 raw-snapshots
test-ingest:
	cd tests/step1 && ./test.sh


## terraform apply para la etapa 2_analysis
tf-apply-2_analysis: build-lambda-analyzer
	cd terraform/stages/2_analysis && terraform apply -var-file="terraform.dev.tfvars"

## terraform destroy para la etapa 2_analysis
tf-destroy-2_analysis:
	cd terraform/stages/2_analysis && terraform destroy -var-file="terraform.dev.tfvars" -auto-approve

## test envia una imagen y pide el record de dynamo db
test-analysis:
	cd tests/step2 && ./test.sh

## destroy all stages (reverse order)
tf-destroy-all: tf-destroy-2_analysis tf-destroy-1_ingest



## Construye el zip de la lambda

build-lambda-snapshot_ingestor:
	cd lambdas/snapshot_ingestor && ./build.sh

## Construye el zip de la lambda

build-lambda-analyzer:
	cd lambdas/analyzer && ./build.sh