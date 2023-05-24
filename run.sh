sudo docker build -t wce-private-cloud .
sudo docker run -v `pwd`/:/app -p 8501:8501 wce-private-cloud


sudo docker run -d --name mongo \
	-e MONGO_INITDB_ROOT_USERNAME=admin \
	-e MONGO_INITDB_ROOT_PASSWORD=admin \
    -v ~/mongo/data:/data/db \
	mongo:latest