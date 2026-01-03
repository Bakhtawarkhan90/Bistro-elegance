FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install Flask mysql-connector-python

ENV MYSQL_HOST=database \
    MYSQL_USER=root \
    MYSQL_PASSWORD=kali \
    MYSQL_DATABASE=table

EXPOSE 5000

CMD ["python", "app.py"]
