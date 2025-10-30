# Makefile para SnapSentinel

.PHONY: test build-lambda


# 0_ingest

## terraform apply para la etapa 1_ingest
tf-apply-1_ingest: build-lambda-snapshot_ingestor
	cd terraform/stages/1_ingest && terraform apply -var-file="terraform.dev.tfvars"

## test envia una imagen a la API Gateway, Lambda la sube a S3 raw-snapshots
test-ingest:
	cd tests/step1 && ./test.sh

## Construye el zip de la lambda

build-lambda-snapshot_ingestor:
	cd lambdas/snapshot_ingestor && ./build.sh
