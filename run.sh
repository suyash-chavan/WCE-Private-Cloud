sudo docker build -t wce-private-cloud .
sudo docker run -v `pwd`/:/app -p 8501:8501 wce-private-cloud