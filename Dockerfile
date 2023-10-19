FROM python:latest

RUN apt-get update -y && \
    apt-get install -y python3-pip python3 python3-dev redis python3-psycopg2

COPY . .

RUN pip3 install pipenv && \
    pip3 install gunicorn psycogp2-binary
RUN python3 -m pipenv install --system
RUN flask db upgrade
CMD ["python3", "-m", "gunicorn", "-w", "4", "app:app", "-b", "0.0.0.0:80"]