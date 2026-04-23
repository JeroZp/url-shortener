output "alb_arn" {
  value = aws_lb.main.arn
}

output "alb_dns_name" {
  description = "Public DNS of the ALB — use this to reach the app"
  value       = aws_lb.main.dns_name
}

output "listener_arn" {
  description = "HTTP listener ARN — required by the blue/green workflow"
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
