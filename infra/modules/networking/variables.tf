variable "project" {
  description = "Nombre del proyecto"
  type        = string
  default     = "url-shortener"
}

variable "environment" {
  description = "Ambiente: staging o production"
  type        = string
  validation {
    condition     = contains(["staging", "production"], var.environment)
    error_message = "El ambiente debe ser 'staging' o 'production'."
  }
}

variable "vpc_cidr" {
  description = "CIDR block para la VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDRs para las subnets públicas"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "AZs donde se crearán las subnets"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "tags" {
  description = "Tags comunes para todos los recursos"
  type        = map(string)
  default     = {}
}