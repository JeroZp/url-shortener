variable "db_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "lab_role_arn" {
  description = "ARN of the AWS Academy LabRole"
  type        = string
}

variable "ecr_backend_url" {
  description = "Backend ECR repository URL"
  type        = string
}

variable "ecr_frontend_url" {
  description = "Frontend ECR repository URL"
  type        = string
}

variable "image_tag" {
  description = "Image tag to deploy"
  type        = string
  default     = "latest"
}

variable "db_password_secret_arn" {
  description = "ARN of the Secrets Manager secret that holds the DB password"
  type        = string
}

variable "tf_state_bucket" {
  description = "Name of the S3 bucket used for remote state"
  type        = string
}