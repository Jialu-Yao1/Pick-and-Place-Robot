# IMM Automation
The imm-automation application is built with docker-compose. Since Docker is being used please ensure that you have Docker Desktop installed on your windows PC for development, it can be downloaded at https://www.docker.com/products/docker-desktop/.
 
In order to execute Docker commands ensure that you have the docker desktop client running. To start the application it first needs to be built. To build the application run the following command: 
```
docker-compose build
```
Once the application has been built it can be run and accessed at http://localhost:8010/. To run the application execute the following command: 

```
docker-compose up -v
```
When the application is to be terminated run the following command: 
```
docker-compose down
```

## Installing Docker on Raspberry PI

Execute the following commands in the terminal:
```
sudo apt update
sudo apt upgrade
sudo reboot
curl -fsSl http://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo groupadd docker
suder usermod -aG docker pi
newgrp docker
```

To verify that Docker installed correctly and can be run without root try and run the hello-world container:

```
docker run hello-world
```

If this container does not run reboot the pi and try running the container again.

## Installing Docker-Compose on Raspberry PI
Since we are specifically using docker-compose to bring up and down our containers it will also need to be installed. This can be done by simply running the following command:
```
sudo apt install docker-compose
```

To enable docker on start up of the raspberry pi run the following command:

```
sudo systemctl enable docker
```

Now any container with a restart policy will re-start automatically on reboot. This will allow the imm-automation application to always be available as long as the raspberry pi is powered on. This will also restart the application in the case of an e-stop.

