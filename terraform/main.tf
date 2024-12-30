provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_instance" "airflow_instance" {
  name         = "suzano-instance"
  machine_type = "e2-standard-2"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-2204-lts"
      size  = 50
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata_startup_script = file("instance_startup_script.sh")

  tags = ["airflow", "docker", "http-server", "https-server"]
}

resource "google_compute_firewall" "allow_airflow" {
  name    = "allow-airflow-webserver"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "7900", "4444", "8081"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_project_service" "enable_bigquery" {
  project            = var.project_id
  service            = "bigquery.googleapis.com"
  disable_on_destroy = false
}

resource "google_storage_bucket" "static-site" {
  name          = "suzano-scraping-data"
  location      = "US"
  force_destroy = true

  uniform_bucket_level_access = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  cors {
    origin          = ["http://image-store.com"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "suzanoinvesting"
  friendly_name               = "suzano"
  description                 = "Dataset para o desafio da suzano"
  location                    = "US"
  default_table_expiration_ms = 3600000
  delete_contents_on_destroy  = true

  labels = {
    env = "default"
  }

  access {
    role          = "OWNER"
    user_by_email = "bqowner@gentle-platform-443802-k8.iam.gserviceaccount.com"
  }

  access {
    role   = "READER"
    domain = "hashicorp.com"
  }
}

output "instance_ip" {
  value = google_compute_instance.airflow_instance.network_interface[0].access_config[0].nat_ip
}
