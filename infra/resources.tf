resource "aws_iam_role" "x_bot_lambda_role" {
  name = "x_bot_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
 }

 data "aws_caller_identity" "current" {}

# Attach basic Lambda execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.x_bot_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_dynamo_policy_attach" {
  role       = aws_iam_role.x_bot_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
} 

resource "aws_iam_role_policy" "lambda_invoke_all" {
  name = "AdditionalPermissions"
  role = aws_iam_role.x_bot_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "lambda:InvokeFunction"
        Resource = "arn:aws:lambda:us-east-1:${data.aws_caller_identity.current.account_id}:function:*"
      },
      {
			"Action": "sqs:sendmessage",
			"Effect": "Allow",
			"Resource": "arn:aws:sqs:us-east-1:${data.aws_caller_identity.current.account_id}:x_bot_api_test_queue"
		  }
    ]
  })
}

resource "aws_dynamodb_table" "posted_tips" {
  name         = "posted_tips"
  billing_mode = "PROVISIONED"
  read_capacity = 1
  write_capacity = 1
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
  tags = {
    Environment = "dev"
    Project     = "x-bot"
  }
}


# Create a ZIP of your code
# data "archive_file" "lambda_zip" {
#  type = "zip"
#  source_dir = "../" # Points to your project root
#  output_path = "fastapi_lambda.zip"
#  excludes = [
#    "terraform/**",
#    ".git/**",
#    ".venv/**",
#    "__pycache__/**",
#    ".env/**",
#  ]
#}

#New approach to packaging lambda with null resurce since I encountered issues with archive_file
resource "null_resource" "lambda_package" {
  triggers = {
    main_py = filebase64sha256("${path.module}/../bot/main.py")
    twitter_client_py = filebase64sha256("${path.module}/../bot/twitter_client.py")
    ai_tweet_generator_py = filebase64sha256("${path.module}/../bot/ai_tweet_generator.py")
    state_py = filebase64sha256("${path.module}/../bot/state.py")
    requirements = filebase64sha256("${path.module}/../bot/requirements.txt")
  }

# Build lambda package
  provisioner "local-exec" {
    command = <<-EOT
      echo "=== Starting Lambda package build ==="
      pwd
      rm -f x_bot_lambda.zip
      rm -rf lambda_package
      mkdir -p lambda_package
      cp ../main.py lambda_package/
      cp ../auth.py lambda_package/
      echo "=== Installing dependencies for Linux platform ==="
      pip install -r ../lambda_reqs.txt -t lambda_package/ --platform linux_x86_64 --only-binary=:all: --no-cache-dir
      echo "=== Creating zip file ==="
      cd lambda_package && zip -r ../x_bot_lambda.zip . && cd ..
      echo "=== Cleaning up ==="
      rm -rf lambda_package
      echo "=== Build complete ==="
    EOT
    working_dir = path.module
  }
}

# Terraform/variables.tf to help us set env variables for Lambda
variable "api_key" {
  description = "API key for authenticated requests"
  type        = string
  sensitive   = true
}

# The actual Lambda function
resource "aws_lambda_function" "x_bot_lambda" {
  depends_on = [null_resource.lambda_package] # Ensure package is built first
  filename = "${path.module}/x_bot_lambda.zip"
  function_name = "x_bot_lambda"
  role = aws_iam_role.x_bot_lambda_role.arn
  handler = "main.handler" # Points to our handler in main.py
  runtime = "python3.11"
  timeout = 30

  environment {
    variables = {
      API_KEY = var.api_key # Set from Terraform variable
      ENVIROMENT = "production"
    }
  }
}