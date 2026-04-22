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

variable "vpc_id" {
  description = "ID de la VPC (del módulo networking)"
  type        = string
}

variable "public_subnet_ids" {
  description = "IDs de las subnets públicas (del módulo networking)"
  type        = list(string)
}

variable "alb_security_group_id" {
  description = "ID del security group del ALB (del módulo networking)"
  type        = string
}

variable "tags" {
  type    = map(string)
  default = {}
}