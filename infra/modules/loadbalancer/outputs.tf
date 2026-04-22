output "alb_arn" {
  value = aws_lb.main.arn
}

output "alb_dns_name" {
  description = "DNS público del ALB — usar este para acceder a la app"
  value       = aws_lb.main.dns_name
}

output "listener_arn" {
  description = "ARN del listener HTTP — necesario para el workflow de blue/green"
  value       = aws_lb_listener.http.arn
}

output "frontend_target_group_arn" {
  value = aws_lb_target_group.frontend.arn
}

output "backend_blue_target_group_arn" {
  value = aws_lb_target_group.backend_blue.arn
}

output "backend_green_target_group_arn" {
  value = aws_lb_target_group.backend_green.arn
}