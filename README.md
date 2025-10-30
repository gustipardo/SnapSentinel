Stages Files Structure:
```
watchfull-ai/
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
│   │
│   ├── modules/
│   │   ├── s3/
│   │   │   └── main.tf
│   │   ├── lambda/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── api-gateway/
│   │   │   └── main.tf
│   │   ├── rekognition/
│   │   │   └── main.tf
│   │   ├── dynamodb/
│   │   │   └── main.tf
│   │   ├── sns/
│   │   │   └── main.tf
│   │   └── iam/
│   │       └── main.tf
│   │
│   └── envs/
│       ├── dev/
│       │   ├── terraform.tfvars
│       │   └── backend.tf
│       └── prod/
│           ├── terraform.tfvars
│           └── backend.tf
│
├── lambdas/
│   ├── snapshot_ingestor/
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── analyzer/
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── event_classifier/
│   │   └── handler.py
│   ├── notifier/
│   │   └── handler.py
│   └── event_api/
│       └── handler.py
│
├── frontend/
│   └── (tu proyecto React/Next.js)
│
└── README.md
```


En el make file andan las tres cosas.
