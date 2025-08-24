# Makefile para SnapSentinel

.PHONY: test build-lambda

# Ejecuta los tests

test:
	cd tests && ./test.sh

# Construye el zip de la lambda

build-lambda:
	cd lambda && ./build.sh
