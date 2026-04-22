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

variable "public_subnet_ids" {
  description = "IDs de las subnets públicas (del módulo networking)"
  type        = list(string)
}

variable "rds_security_group_id" {
  description = "ID del security group de RDS (del módulo networking)"
  type        = string
}

variable "redis_security_group_id" {
  description = "ID del security group de Redis (del módulo networking)"
  type        = string
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
  default     = "urlshortener"
}

variable "db_username" {
  description = "Usuario de la base de datos"
  type        = string
  default     = "urlshortener"
}

variable "db_password" {
  description = "Contraseña de la base de datos — pasar desde tfvars o secrets"
  type        = string
  sensitive   = true
}

variable "tags" {
  type    = map(string)
  default = {}
}