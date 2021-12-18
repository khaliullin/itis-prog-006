docker


docker images


# containers
docker ps
docker ps -a


# Dockerfile #
```
FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py", "-p 8000"]
```



# build image using Dockerfile
docker build -t image_name .


# Run container by image
docker run --name -p 5000:5000 container_name image_name


docker start <id/name>
docker stop <id/name>


# run command inside container
docker exec -it <id/name> /bin/bash
docker exec -it <id/name> flask db init
docker exec -it <id/name> pip install -r requirements.txt


docker logs <id/name>


docker attach <id/name>



# docker-compose.yml #

```
version: '3'
services:
    web:
        build: .
        ports:
            - "8000:8000"
        volumes:
          - .:/app
        restart: always
    db:
        image: postgres:9.6
        restart: always
        container_name: postgres_db_container
        environment:
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
            POSTGRES_DB: flask
        ports:
            - "5432:5432"
```
