FROM python:3.8

RUN apt-get update
RUN apt-get -y install libhdf5-dev

RUN pip install --upgrade pip setuptools wheel
# layer caching for faster builds
COPY requirements.txt /
RUN pip install -r /requirements.txt

#COPY app.py /app.py
ADD . /worker
WORKDIR /worker

ENTRYPOINT celery -A tasks worker --loglevel=info
#-Q celery_worker
#ENTRYPOINT ['celery','-A','test_celery', 'worker', '--loglevel=info']
