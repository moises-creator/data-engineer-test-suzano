variable "project_id" {
  description = "ID do projeto no GCP"
  type        = string
}

variable "region" {
  description = "Região para os recursos"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Zona para os recursos"
  type        = string
  default     = "us-central1-a"
}
