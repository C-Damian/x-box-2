terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "aws" {
  region = var.aws_region
  
  # This will automatically use:
  # - Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) in GitHub Actions
  # - Local AWS profile when running locally
  # No need to specify profile explicitly
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}