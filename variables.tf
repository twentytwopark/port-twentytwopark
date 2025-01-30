variable "port_client_id" {
  type        = string
  description = "Port.io Client ID"
}

variable "port_client_secret" {
  type        = string
  description = "Port.io Client Secret"
  sensitive   = true
}

variable "github_org" {
  type        = string
  description = "GitHub organization name"
}

variable "github_repo" {
  type        = string
  description = "GitHub repository name"
}
