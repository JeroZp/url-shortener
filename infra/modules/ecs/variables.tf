variable "project" {
  type    = string
  default = "url-shortener"
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["staging", "production"], var.environment)
    error_message = "environment must be 'staging' or 'production'."
  }
}

variable "lab_role_arn" {
  description = "ARN of the preexisting AWS Academy LabRole"
  type        = string
}

variable "ecr_backend_url" {
  description = "Backend ECR repository URL (without tag)"
  type        = string
}

variable "ecr_frontend_url" {
  description = "Frontend ECR repository URL (without tag)"
  type        = string
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}

variable "public_subnet_ids" {
  type = list(string)
}

variable "ecs_backend_security_group_id" {
  type = string
}

variable "ecs_frontend_security_group_id" {
  type = string
}

variable "backend_blue_target_group_arn" {
  type = string
}

variable "backend_green_target_group_arn" {
  description = "Green target group ARN for blue/green backend deployments"
  type        = string
  default     = ""
}

variable "frontend_target_group_arn" {
  type = string
}

variable "alb_dns_name" {
  description = "ALB DNS — injected into the frontend as VITE_API_URL"
  type        = string
}

# --- Database ---
variable "db_host" {
  type = string
}

variable "db_name" {
  type    = string
  default = "urlshortener"
}

variable "db_username" {
  type    = string
  default = "urlshortener"
}

variable "db_password_secret_arn" {
  description = "ARN of the Secrets Manager secret that holds the DB password"
  type        = string
}

variable "redis_host" {
  type = string
}

variable "redis_port" {
  type    = number
  default = 6379
}

# --- Sizing ---
variable "backend_cpu" {
  type    = number
  default = 256
}

variable "backend_memory" {
  type    = number
  default = 512
}

variable "frontend_cpu" {
  type    = number
  default = 256
}

variable "frontend_memory" {
  type    = number
  default = 512
}

variable "backend_desired_count" {
  type    = number
  default = 1
}

variable "frontend_desired_count" {
  type    = number
  default = 1
}

variable "tags" {
  type    = map(string)
  default = {}
}
