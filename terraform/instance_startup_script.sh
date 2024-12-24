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


if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "Gerando chave SSH..."
    ssh-keygen -t ed25519 -C "moises.ximenes5@gmail.com" -f ~/.ssh/id_ed25519 -q -N ""
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519

    echo "Adicione a seguinte chave pública ao GitHub (SSH):"
    cat ~/.ssh/id_ed25519.pub
    echo "Abortando script para configurar a chave no GitHub."
    exit 1
fi

ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts


git clone https://github.com/moises-creator/data-engineer-test-suzano.git
cd data-engineer-test-suzano

mkdir -p include/csv
chmod -R 775 include/csv 

PROJECT_ID="gentle-platform-443802-k8" 
SERVICE_ACCOUNT="bqowner@$PROJECT_ID.iam.gserviceaccount.com"
KEY_FILE="/home/$USER/bqowner-key.json"

gcloud iam service-accounts keys create $KEY_FILE --iam-account $SERVICE_ACCOUNT


echo "export GOOGLE_APPLICATION_CREDENTIALS=$KEY_FILE" >> ~/.bashrc
source ~/.bashrc

pip install apache-airflow-providers-google

astro dev start

export AIRFLOW_HOME=$(pwd)/airflow 
airflow connections add google_cloud_default \
    --conn-type google_cloud_platform \
    --conn-extra "{\"extra__google_cloud_platform__key_path\": \"$KEY_FILE\", \"extra__google_cloud_platform__project\": \"$PROJECT_ID\"}"
