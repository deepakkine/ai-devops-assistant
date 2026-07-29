terraform {
  backend "s3" {
    bucket         = "ai-devops-assistant-dev-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "ai-devops-assistant-dev-terraform-lock"
    encrypt        = true
  }
}