FROM python:latest

RUN apt-get update -y && \
    apt-get install -y python3-pip python3 python3-dev redis

COPY . .

RUN pip3 install pipenv && \
    pip3 install gunicorn
RUN python3 -m pipenv install --system
RUN flask db upgrade
CMD ["python3", "-m", "gunicorn", "-w", "4", "app:app", "-b", "0.0.0.0:80"]