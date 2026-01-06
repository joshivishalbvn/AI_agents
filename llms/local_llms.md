# Offline Models Which Need Good Amount Of Hardware

# DeepSeek-R1
# Qwen 3
# Llama 3.3
# Qwen 2.5-VL
# Gemma 3
# Many Others


# can download to local machine or using docker


# download docker image : 


# to run it we need web-UI = https://docs.openwebui.com/getting-started/quick-start/ : Quick Start with Docker part 


# docker container ps

# stop container = sudo docker container stop 91e637011c4e
# start container = sudo docker container start 13cb17445332
    

"""
docker container ps
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS                                             NAMES
5f54beb12ebd   ollama/ollama   "/bin/ollama serve"      4 seconds ago   Up 3 seconds   0.0.0.0:11434->11434/tcp, [::]:11434->11434/tcp   ollama
13cb17445332   redis:latest    "docker-entrypoint.s…"   2 weeks ago     Up 5 hours     6379/tcp                                          weather-main_redis_1
~$ sudo docker inspect --format '{{.State.Pid}}' 5f54beb12ebd
54682
~$ sudo kill -9 54682
sudo docker rm -f ollama


and now again start :
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

docker start portainer
docker start ollama

"""