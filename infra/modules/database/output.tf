output "db_endpoint" {
  description = "Endpoint de conexión a RDS (host:port)"
  value       = aws_db_instance.postgres.endpoint
}

output "db_host" {
  description = "Host de RDS sin puerto"
  value       = aws_db_instance.postgres.address
}

output "db_name" {
  value = aws_db_instance.postgres.db_name
}

output "db_username" {
  value = aws_db_instance.postgres.username
}

output "redis_endpoint" {
  description = "Endpoint de conexión a Redis"
  value       = aws_elasticache_cluster.redis.cache_nodes[0].address
}

output "redis_port" {
  value = aws_elasticache_cluster.redis.port
}