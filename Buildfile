docker build -t flask .
docker tag flask bmjduncan/flask
docker push bmjduncan/flask
docker stop flask
docker rm flask

