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

variable "vpc_id" {
  description = "VPC ID (from the networking module)"
  type        = string
}

variable "public_subnet_ids" {
  description = "IDs of the public subnets (from the networking module)"
  type        = list(string)
}

variable "alb_security_group_id" {
  description = "ALB security group ID (from the networking module)"
  type        = string
}

variable "tags" {
  type    = map(string)
  default = {}
}
