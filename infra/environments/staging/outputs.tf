output "alb_dns_name" {
  description = "Public DNS of the staging ALB (input for smoke tests)"
  value       = module.loadbalancer.alb_dns_name
}

output "ecs_cluster_name" {
  description = "ECS cluster name — used by deploy/rollback workflows"
  value       = module.ecs.cluster_name
}

output "backend_service_name" {
  value = module.ecs.backend_service_name
}

output "frontend_service_name" {
  value = module.ecs.frontend_service_name
}

output "backend_task_definition_family" {
  value = module.ecs.backend_task_definition_family
}

output "frontend_task_definition_family" {
  value = module.ecs.frontend_task_definition_family
}
