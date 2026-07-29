variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project Name"
  type        = string
  default     = "ai-devops-assistant"
}

variable "environment" {
  description = "Deployment Environment"
  type        = string
  default     = "dev"
}