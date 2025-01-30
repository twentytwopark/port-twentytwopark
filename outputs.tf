output "port_action_id" {
  value       = port_action.restart_argocd_app.id
  description = "The ID of the created Port.io action"
}
