🧪 Guía de Ejecución de Tests - SnapSentinel

Esta guía detalla paso a paso cómo ejecutar las pruebas automatizadas del proyecto. Cubre desde la configuración del entorno hasta la ejecución de pruebas unitarias (locales) y de integración (AWS real).

✅ 1. Prerrequisitos

Antes de empezar, asegúrate de tener instalado:

Python 3 (versión 3.9 o superior recomendada).

AWS CLI configurado o tener tus credenciales a mano (necesario solo para tests de integración).

Configuración de Credenciales AWS

Para los Integration Tests, el sistema necesita permiso para hablar con tu cuenta AWS (dev).
Asegúrate de tener las variables de entorno configuradas o tu archivo ~/.aws/credentials listo.

export AWS_ACCESS_KEY_ID="tu_access_key"
export AWS_SECRET_ACCESS_KEY="tu_secret_key"
export AWS_DEFAULT_REGION="us-east-1"  # O tu región preferida


🛠️ 2. Configuración del Entorno (Solo la primera vez)

Para no mezclar librerías, crearemos un entorno virtual e instalaremos lo necesario.

Crear el entorno virtual:

python3 -m venv .venv


Activar el entorno:

En Mac/Linux:

source .venv/bin/activate


En Windows:

.venv\Scripts\activate


Instalar dependencias de test:
Este comando instala pytest, boto3, moto y otras herramientas listadas en el archivo de requerimientos.

pip install -r tests/requirements.txt


🧱 3. Ejecutar Unit Tests (Rápidos y Locales)

Estos tests prueban la lógica de las Lambdas sin conectar a Internet ni a AWS. Usan moto para simular S3 y DynamoDB. Son ideales para correr mientras programas.

Comando:

pytest tests/unit


Qué esperar:
Deberías ver una salida indicando que los componentes (Ingestor, Analyzer, Classifier) pasaron correctamente.

tests/unit/test_analyzer.py .           [ 25%]
tests/unit/test_event_classifier.py ..  [ 75%]
tests/unit/test_snapshot_ingestor.py .  [100%]

================ 4 passed in 0.46s ================


🔗 4. Ejecutar Integration Tests (AWS Real)

Estos tests sí conectan a AWS. Prueban que el flujo funcione realmente en la nube en el entorno de dev.

⚠️ Importante: Requiere credenciales activas de AWS.

Comando estándar:

pytest tests/integration


Comando para depuración (No borrar recursos):
Si quieres ver los archivos en S3 o los datos en DynamoDB después del test (para inspeccionar errores), usa:

pytest tests/integration --keep-resources


¿Qué se está probando?

El test corre en 3 etapas secuenciales:

Stage 1 (Ingest): test_stage_1_ingest.py

Sube una imagen vía API Gateway real.

Verifica que llegue al bucket snapsentinel-images-dev.

Stage 2 (Analysis): test_stage_2_analysis.py

Verifica que al subir la imagen, la Lambda Analyzer se active.

Revisa que los resultados del análisis se escriban en DynamoDB (analysis_results-dev).

Stage 3 (Classification): test_stage_3_classification.py

Simula la inserción de un registro crítico en DynamoDB.

Verifica que la Lambda Classifier procese la alerta (revisando logs de CloudWatch o estado final).

Resultado esperado:

tests/integration/test_stage_1_ingest.py .        [ 33%]
tests/integration/test_stage_2_analysis.py .      [ 66%]
tests/integration/test_stage_3_classification.py .[100%]

================ 3 passed in 17.67s ================


🆘 Solución de Problemas Comunes

Error NoCredentialsError:

Solución: No has configurado tus credenciales de AWS. Revisa el paso 1.

Error ModuleNotFoundError: No module named 'pytest':

Solución: No activaste el entorno virtual o olvidaste hacer pip install. Revisa el paso 2.

Tests fallan en Integration:

Solución: Asegúrate de que has desplegado la infraestructura a dev (terraform apply) antes de correr estos tests, ya que buscan recursos reales existentes.

🚀 5. Ejecutar End-to-End (E2E) Tests (Flujo Completo)

Estos tests verifican el flujo completo del sistema desde el inicio hasta el final, simulando un escenario real de uso.

⚠️ Importante: Requiere credenciales activas de AWS y la infraestructura desplegada en dev.

Comando estándar:

```bash
pytest tests/e2e
```

¿Qué se está probando?

El test E2E (`test_full_flow.py`) ejecuta el pipeline completo:

1. **Input**: Envía una imagen "crítica" (ej: persona encapuchada) al API Gateway.
2. **Procesamiento**: Espera a que el sistema complete todo el flujo:
   - API Gateway → S3
   - S3 → Lambda Analyzer → Rekognition → DynamoDB
   - DynamoDB Stream → Lambda Classifier → SNS
3. **Verificación**: Confirma que aparece el log "Publishing to SNS" en CloudWatch Logs.

Resultado esperado:

```
tests/e2e/test_full_flow.py .                    [100%]

================ 1 passed in 16.68s ================
```

📝 6. Comandos Makefile (Atajos)

Para facilitar la ejecución, puedes usar estos comandos desde la raíz del proyecto:

```bash
make test-unit           # Ejecuta tests unitarios
make test-integration    # Ejecuta tests de integración
make test-e2e           # Ejecuta tests E2E
make deploy-dev         # Despliega toda la infraestructura a dev
```