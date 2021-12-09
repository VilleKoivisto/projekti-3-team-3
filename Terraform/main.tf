# Projekti / ryhmä 3 / Terraform-template
# -----------------------------------------------
# Templaten muuttujat määritellään tiedostossa "variables.tf"

# Provider-tiedot:
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
}

# Luodaan bucket-resurssi
resource "google_storage_bucket" "bucket" {
  name     = "projekti-fileet-2"
  location = "US"
}

# FUNKTIO LUODAAN TÄSSÄ
# -------------------------------------------------------------------------------------------

# haetaan zipattu funktio lokalista
# zipin sisällä:
# - main.py
# - requirements.txt
resource "google_storage_bucket_object" "archive" {
  name   = "testifunktio.zip"
  bucket = google_storage_bucket.bucket.name
  source = "../Funktio-temp/testifunktio.zip"
}

# luodaan funktio bucketista löytyvästä zipistä
resource "google_cloudfunctions_function" "function" {
  name        = "testi-funktio-terraform"
  description = "testataan terraformia ja funktion luomista"
  runtime     = "python39"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  entry_point           = "get_temp"
}
# -------------------------------------------------------------------------------------------