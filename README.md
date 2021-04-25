# flask-mysql

```
docker build -t flaskapi .

docker run -d -p 8080:8080 flaskapi

curl -X POST http://localhost:8080/INSERT?name=&lastName=&mail=

curl -X DELETE http://localhost:8080/DELETE?name=

curl http://localhost:8080/SELECT?lastName=
```
