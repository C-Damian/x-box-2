x-bot-2/
│
├── bot/                    # Core Python bot logic (modular, testable)
│   ├── __init__.py
│   ├── main.py             # Lambda entrypoint
│   ├── categories.py       # Category logic
│   ├── tweet_generator.py  # AI/template tweet generation
│   ├── twitter_client.py   # Twitter API integration
│   ├── state.py            # S3/DynamoDB state tracking
│   └── config.py           # Env var/secrets loading
│
├── tests/                  # Unit/integration tests
│   └── test_main.py
│
├── infra/                  # Terraform IaC
│   ├── main.tf
│   ├── lambda.tf
│   ├── eventbridge.tf
│   ├── s3.tf / dynamodb.tf
│   ├── iam.tf
│   └── variables.tf
│
├── Dockerfile              # For local testing (optional)
├── requirements.txt        # Python dependencies
├── .env.example            # Example env vars for local dev
├── README.md
└── .gitignore

