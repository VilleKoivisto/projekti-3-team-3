# Projekti / ryhmä 3 / Terraformin muuttujat
# --------------------------------------------------

# Nämä haetaan terraform.tfvars-tiedostosta:
variable "project" {}

variable "credentials_file" {}

# Nämä määritellään tässä:
variable "region" {
  default = "us-central1"
}

variable "zone" {
  default = "us-central1-a"
}