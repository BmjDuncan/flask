docker build -t flask .
docker tag flask bmjduncan/flask
docker push bmjduncan/flask
docker stop flask
docker rm flask
docker stop some-mysql
docker rm some-mysql
docker run -p 3306:3306 --name some-mysql -e MYSQL_ROOT_PASSWORD=dacjd156n. -d mysql:8.0
docker run -p 80:5000 -d --name flask --link some-mysql:some-mysql bmjduncan/flask
