output "identity_center_instance_arns" {
  description = "ARNs of IAM Identity Center instances"
  value       = data.aws_ssoadmin_instances.this.arns
}
output "identity_store_ids" {
  description = "Identity Store IDs for IAM Identity Center"
  value       = data.aws_ssoadmin_instances.this.identity_store_ids
}