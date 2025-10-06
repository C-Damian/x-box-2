## Project Overview

**X-Bot** is a cloud-native, automated Twitter bot that posts daily, AI-generated tech tips based on a rotating category. The bot leverages Google Gemini for content generation and posts directly to Twitter using the official API. State management is handled via AWS (S3 or DynamoDB), ensuring no repeated tips.

### Why I Built This

This is a personal project for hands-on practice with:
- Python scripting and modular design
- AWS serverless architecture (Lambda, EventBridge, S3/DynamoDB)
- Infrastructure as Code with Terraform
- Secure secrets management
- Automated deployment pipelines with GitHub Actions
- AI integration for real-world automation

The goal is to learn by doing, experiment with best practices, and build a foundation for future, more complex cloud-native apps.

## Continuous Integration & Deployment

This project now uses **GitHub Actions** for automated CI/CD. On every push to `main`, the workflow builds, tests, and deploys the AWS infrastructure using Terraform. This setup is ideal for practicing modern DevOps workflows and cloud automation.
```bash
x-bot-2/
│
├── bot/                    # Core Python bot logic (modular, testable)
│   ├── __init__.py
│   ├── main.py             # Lambda entrypoint
│   ├── categories.py       # Category logic
│   ├── tweet_generator.py  # AI/template tweet generation
│   ├── twitter_client.py   # Twitter API integration 
│   └── state.py            # S3/DynamoDB state tracking
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
├── requirements.txt        # Python dependencies
├── .env.example            # Example env vars for local dev
├── README.md
└── .gitignore
```


### Features

- **Daily AI-Generated Tweets:**  
	Posts practical, developer-focused tips in categories like Python, JavaScript, DevOps, Git, Performance, Security, and APIs.

- **Cloud-Native Automation:**  
	Runs as an AWS Lambda function, triggered daily by AWS EventBridge (cron scheduler).

- **State Tracking:**  
	Uses AWS S3 or DynamoDB to track posted tips and prevent repeats.

- **Secure Secrets Management:**  
	API keys and secrets are managed via environment variables or AWS Secrets Manager.

- **Modular Python Codebase:**  
	Core logic is organized for easy extension (e.g., new categories, platforms, or a future API/frontend).

### Tech Stack

- **Python 3.x** (core bot logic)
- **AWS Lambda** (serverless compute)
- **AWS EventBridge** (scheduled triggers)
- **AWS S3 / DynamoDB** (state management)
- **Terraform** (infrastructure as code)
- **Google Gemini API** (AI content generation)
- **Twitter API** (tweet posting)

### Infrastructure & Deployment

- **Provisioning:**  
	All AWS resources (Lambda, EventBridge, S3/DynamoDB, IAM roles/policies) are defined and managed using Terraform, located in the `infra/` directory.

- **Deployment:**  
	Lambda deployment package is built and uploaded via Terraform. Environment variables and secrets are configured in AWS.

- **Local Testing:**  
	Dockerfile will be provided for simulating Lambda locally. Unit tests will be in the `tests/` directory.

### Next Steps

- **Extensibility:**  
	The codebase is designed for future expansion, such as adding a FastAPI backend, web UI, or support for additional social platforms.
