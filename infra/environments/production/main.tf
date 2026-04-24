# =============================================================================
# Production ENVIRONMENT — url-shortener
# =============================================================================

terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "url-shortener-tfstate-eafit-g3-v1"
    key    = "production/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

locals {
  tags = {
    Project     = "url-shortener"
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

module "networking" {
  source      = "../../modules/networking"
  project     = "url-shortener"
  environment = "production"
  tags        = local.tags
}

module "database" {
  source                  = "../../modules/database"
  project                 = "url-shortener"
  environment             = "production"
  public_subnet_ids       = module.networking.public_subnet_ids
  rds_security_group_id   = module.networking.rds_security_group_id
  redis_security_group_id = module.networking.redis_security_group_id
  db_password             = var.db_password
  tags                    = local.tags
}

module "loadbalancer" {
  source                = "../../modules/loadbalancer"
  project               = "url-shortener"
  environment           = "production"
  vpc_id                = module.networking.vpc_id
  public_subnet_ids     = module.networking.public_subnet_ids
  alb_security_group_id = module.networking.alb_security_group_id
  tags                  = local.tags
}

module "ecs" {
  source                         = "../../modules/ecs"
  project                        = "url-shortener"
  environment                    = "production"
  lab_role_arn                   = var.lab_role_arn
  ecr_backend_url                = var.ecr_backend_url
  ecr_frontend_url               = var.ecr_frontend_url
  image_tag                      = var.image_tag
  public_subnet_ids              = module.networking.public_subnet_ids
  ecs_backend_security_group_id  = module.networking.ecs_backend_security_group_id
  ecs_frontend_security_group_id = module.networking.ecs_frontend_security_group_id
  backend_blue_target_group_arn  = module.loadbalancer.backend_blue_target_group_arn
  backend_green_target_group_arn = module.loadbalancer.backend_green_target_group_arn
  frontend_target_group_arn      = module.loadbalancer.frontend_target_group_arn
  alb_dns_name                   = module.loadbalancer.alb_dns_name
  db_host                        = module.database.db_host
  db_name                        = module.database.db_name
  db_username                    = module.database.db_username
  db_password_secret_arn         = var.db_password_secret_arn
  redis_host                     = module.database.redis_endpoint
  redis_port                     = module.database.redis_port
  tags                           = local.tags
}