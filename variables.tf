variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "OAUTH_CLIENT_ID" {
  description = "OAUTH Client id"
  type        = string
  sensitive   = true
}

variable "OAUTH_CLIENT_SECRET" {
  description = "OAUTH Client Secret"
  type        = string
  sensitive   = true
}
