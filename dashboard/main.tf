provider "aws" {
  region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY 
}

resource "aws_ecr_repository" "dashboard_ecr" {
  name = "kelpie-plants-dashboard"
  image_scanning_configuration {
    scan_on_push = true
  }

  image_tag_mutability = "MUTABLE"
}

resource "aws_ecs_cluster" "dashboard_ecs" {
  name = "kelpie-plants-dashboard"
}

output "repository_url" {
  value = aws_ecr_repository.example.repository_url
}