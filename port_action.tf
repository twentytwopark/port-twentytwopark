resource "port_action" "restart_argocd_app" {
  title      = "Restart Argo CD Application"
  identifier = "restart-argocd-application"
  icon       = "Argo"
  
  self_service_trigger = {
    operation            = "DAY-2"
    blueprint_identifier = "argocdApplication"
    user_properties = {
      string_props = {
        application_name = {
          title    = "Application Name"
          required = true
          format   = "entity"
          blueprint = "argocdApplication"
          dataset = {
            combinator = "and"
            rules = [{
              property = "$title"
              operator = "="  # Changed to supported operator
              value    = { 
                jq_query = "true"  # Always true condition
              }
            }]
          }
          sort = {
            property = "$updatedAt"
            order    = "DESC"
          }
        }
      }
      boolean_props = {
        confirm_restart = {
          title    = "Confirm Restart"
          required = true
        }
      }
    }
  }

  github_method = {
    org      = var.github_org
    repo     = var.github_repo
    workflow = "restart-argocd-app.yaml"
    omit_payload = false
    omit_user_inputs = false
  }
}
