FROM python:3.7-slim-buster

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get install -y python3-dev && \
    apt-get install -y libpq-dev && \
    apt-get install -y vim && \
    apt-get clean

ENV TZ Asia/Bangkok

WORKDIR /code
ADD . /code
# COPY . /code

# install requirements
RUN pip install gunicorn
RUN pip install -r requirements.txt



CMD ["python", "app.py"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5555", "--workers", "2", "--threads", "4", "--worker-class", "gthread", "app:app"]
EXPOSE 3515
