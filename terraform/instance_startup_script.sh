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

docker run -d \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/bqowner-key.json \
  -v /home/$USER/bqowner-key.json:/app/bqowner-key.json \
  moises-creator/data-engineer-test-suzano:latest  

export AIRFLOW_HOME=$(pwd)/airflow  
airflow connections add google_cloud_default \
    --conn-type google_cloud_platform \
    --conn-extra "{\"extra__google_cloud_platform__key_path\": \"/app/bqowner-key.json\", \"extra__google_cloud_platform__project\": \"$PROJECT_ID\"}"