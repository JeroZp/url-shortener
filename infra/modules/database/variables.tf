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

variable "public_subnet_ids" {
  description = "IDs of the public subnets (from the networking module)"
  type        = list(string)
}

variable "rds_security_group_id" {
  description = "RDS security group ID (from the networking module)"
  type        = string
}

variable "redis_security_group_id" {
  description = "Redis security group ID (from the networking module)"
  type        = string
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "urlshortener"
}

variable "db_username" {
  description = "Database user"
  type        = string
  default     = "urlshortener"
}

variable "db_password" {
  description = "Database password — pass from tfvars or secrets"
  type        = string
  sensitive   = true
}

variable "tags" {
  type    = map(string)
  default = {}
}
