variable "db_password" {
  description = "Contraseña de PostgreSQL"
  type        = string
  sensitive   = true
}

variable "lab_role_arn" {
  description = "ARN del LabRole de AWS Academy"
  type        = string
}

variable "ecr_backend_url" {
  description = "URL del repositorio ECR del backend"
  type        = string
}

variable "ecr_frontend_url" {
  description = "URL del repositorio ECR del frontend"
  type        = string
}

variable "image_tag" {
  description = "Tag de la imagen a desplegar"
  type        = string
  default     = "latest"
}

variable "db_password_secret_arn" {
  description = "ARN del secret en Secrets Manager con la contraseña de la DB"
  type        = string
}

variable "tf_state_bucket" {
  description = "Nombre del bucket S3 para el remote state"
  type        = string
}