variable "project" {
  type    = string
  default = "url-shortener"
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["staging", "production"], var.environment)
    error_message = "El ambiente debe ser 'staging' o 'production'."
  }
}

variable "lab_role_arn" {
  description = "ARN del LabRole preexistente en AWS Academy"
  type        = string
}

variable "ecr_backend_url" {
  description = "URL del repositorio ECR del backend (sin tag)"
  type        = string
}

variable "ecr_frontend_url" {
  description = "URL del repositorio ECR del frontend (sin tag)"
  type        = string
}

variable "image_tag" {
  description = "Tag de la imagen Docker a desplegar"
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

variable "frontend_target_group_arn" {
  type = string
}

variable "alb_dns_name" {
  description = "DNS del ALB — se inyecta al frontend como VITE_API_URL"
  type        = string
}

# --- Base de datos ---
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
  description = "ARN del secret en Secrets Manager con la contraseña de la DB"
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