# Makefile para SnapSentinel
.PHONY: build-lambda-snapshot_ingestor build-lambda-analyzer build-lambda-event_classifier \
        tf-apply-1_ingest tf-destroy-1_ingest test-ingest \
        tf-apply-2_analysis tf-destroy-2_analysis test-analysis \
        tf-apply-3_classification tf-destroy-3_classification test-classification \
        tf-destroy-all

# Default environment is dev. Override with make ENV=prod <target>
ENV ?= dev

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
# Stage 1: Ingest
########################################

## terraform apply para la etapa 1_ingest
tf-apply-1_ingest: build-lambda-snapshot_ingestor
	cd terraform/stages/1_ingest && \
	terraform init -reconfigure -backend-config="key=env/$(ENV)/ingest/terraform.tfstate" && \
	terraform apply -var-file="$(ENV).tfvars" -auto-approve

## terraform destroy para la etapa 1_ingest
tf-destroy-1_ingest:
	cd terraform/stages/1_ingest && \
	terraform init -reconfigure -backend-config="key=env/$(ENV)/ingest/terraform.tfstate" && \
	terraform destroy -var-file="$(ENV).tfvars" -auto-approve

## test envia una imagen a la API Gateway, Lambda la sube a S3 raw-snapshots
test-ingest:
	cd tests/step1 && ./test.sh

########################################
# Stage 2: Analysis
########################################

## terraform apply para la etapa 2_analysis
tf-apply-2_analysis: build-lambda-analyzer
	cd terraform/stages/2_analysis && \
	terraform init -reconfigure -backend-config="key=env/$(ENV)/analysis/terraform.tfstate" && \
	terraform apply -var-file="$(ENV).tfvars" -auto-approve

## terraform destroy para la etapa 2_analysis
tf-destroy-2_analysis:
	cd terraform/stages/2_analysis && \
	terraform init -reconfigure -backend-config="key=env/$(ENV)/analysis/terraform.tfstate" && \
	terraform destroy -var-file="$(ENV).tfvars" -auto-approve

## test envia una imagen y pide el record de dynamo db
test-analysis:
	cd tests/step2 && ./test.sh

########################################
# Stage 3: Classification
########################################

## terraform apply para la etapa 3_classification
tf-apply-3_classification: build-lambda-event_classifier
	cd terraform/stages/3_classification && \
	terraform init -reconfigure -backend-config="key=env/$(ENV)/classification/terraform.tfstate" && \
	terraform apply -var-file="$(ENV).tfvars" -auto-approve

## terraform destroy para la etapa 3_classification
tf-destroy-3_classification:
	cd terraform/stages/3_classification && \
	terraform init -reconfigure -backend-config="key=env/$(ENV)/classification/terraform.tfstate" && \
	terraform destroy -var-file="$(ENV).tfvars" -auto-approve

## test classification logic
test-classification:
	cd tests/step3 && ./test.sh

########################################
# Apply all stages
########################################

tf-apply-all: tf-apply-1_ingest tf-apply-2_analysis tf-apply-3_classification

########################################
# Destroy all stages (reverse order)
########################################

tf-destroy-all: tf-destroy-3_classification tf-destroy-2_analysis tf-destroy-1_ingest
