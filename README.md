# flask-mysql

```
docker build -t flaskapi .

docker run -d -p 8080:8080 flaskapi

curl -x POST http://localhost:8080/INSERT?name=&lastName=&mail=

curl -x DELETE http://localhost:8080/DELETE?name=

curl http://localhost:8080/SELECT
```
