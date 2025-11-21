# Makefile para SnapSentinel
.PHONY: build-lambda test tf-apply tf-destroy tf-destroy-all

########################################
# General build targets
########################################

## Construye todas las lambdas
build-lambda-snapshot_ingestor:
	cd lambdas/snapshot_ingestor && ./build.sh

build-lambda-analyzer:
	cd lambdas/analyzer && ./build.sh

build-lambda-event_classifier:
	cd lambdas/event_classifier && ./build.sh

########################################
# Stage 0_ingest
########################################

## terraform apply para la etapa 1_ingest
tf-apply-1_ingest: build-lambda-snapshot_ingestor
	cd terraform/stages/1_ingest && terraform apply -var-file="terraform.dev.tfvars" -auto-approve

## terraform destroy para la etapa 1_ingest
tf-destroy-1_ingest:
	cd terraform/stages/1_ingest && terraform destroy -var-file="terraform.dev.tfvars" -auto-approve

## test envia una imagen a la API Gateway, Lambda la sube a S3 raw-snapshots
test-ingest:
	cd tests/step1 && ./test.sh

########################################
# Stage 2_analysis
########################################

## terraform apply para la etapa 2_analysis
tf-apply-2_analysis: build-lambda-analyzer
	cd terraform/stages/2_analysis && terraform apply -var-file="terraform.dev.tfvars" -auto-approve

## terraform destroy para la etapa 2_analysis
tf-destroy-2_analysis:
	cd terraform/stages/2_analysis && terraform destroy -var-file="terraform.dev.tfvars" -auto-approve

## test envia una imagen y pide el record de dynamo db
test-analysis:
	cd tests/step2 && ./test.sh

########################################
# Stage 3_classification
########################################

## terraform apply para la etapa 3_classification
tf-apply-3_classification: build-lambda-event_classifier
	cd terraform/stages/3_classification && terraform init && terraform apply -auto-approve

## terraform destroy para la etapa 3_classification
tf-destroy-3_classification:
	cd terraform/stages/3_classification && terraform destroy -auto-approve

## test classification logic
test-classification:
	cd tests/step3 && ./test.sh

########################################
# Destroy all stages (reverse order)
########################################

tf-destroy-all: tf-destroy-3_classification tf-destroy-2_analysis tf-destroy-1_ingest
