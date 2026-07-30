output "instance_id" {
  description = "EC2 Instance ID"
  value       = module.compute.instance_id
}

output "public_ip" {
  description = "Elastic IP"
  value       = module.compute.public_ip
}

output "public_dns" {
  description = "Public DNS"
  value       = module.compute.public_dns
}

output "repository_name" {
  description = "ECR Repository Name"
  value       = module.ecr.repository_name
}

output "ecr_repository_url" {
  description = "ECR Repository URL"
  value       = module.ecr.repository_url
}