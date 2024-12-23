sudo apt-get update && sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    gnupg \
    unzip \
    python3-pip \
    git

sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker $USER


curl -sSL https://install.astronomer.io | sudo bash


git clone https://github.com/moises-creator/data-engineer-test-suzano.git
cd data-engineer-test-suzano


PROJECT_ID="gentle-platform-443802-k8"
SERVICE_ACCOUNT="bqowner@$PROJECT_ID.iam.gserviceaccount.com"
KEY_FILE="/home/$USER/bqowner-key.json"


gcloud iam service-accounts keys create $KEY_FILE --iam-account $SERVICE_ACCOUNT

echo "export GOOGLE_APPLICATION_CREDENTIALS=$KEY_FILE" >> ~/.bashrc
source ~/.bashrc

pip install apache-airflow-providers-google

astro dev start
