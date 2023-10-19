FROM python:latest

RUN apt-get update -y && \
    apt-get install -y python3-pip python3 python3-dev redis python3-psycopg2

COPY . .

RUN pip3 install pipenv && \
    pip3 install gunicorn psycopg2-binary
RUN python3 -m pipenv install --system
ENTRYPOINT "flask db upgrade && python3 -m gunicorn -w 4 app:app -b 0.0.0.0:80"