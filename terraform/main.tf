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
    ports    = ["8080", "80", "443", "7900", "4444"] 
  }

  source_ranges = ["0.0.0.0/0"] 
}

output "instance_ip" {
  value = google_compute_instance.airflow_instance.network_interface[0].access_config[0].nat_ip
}
