FROM python:3.9-slim-bullseye

# layer caching for faster builds
COPY requirements.txt /
RUN pip install -r /requirements.txt


ADD . /doodler
WORKDIR /doodler

ENV FLASK_ENV=development

CMD flask run --host=0.0.0.0

#CMD gunicorn --workers $WORKERS \
#  --threads $THREADS \
#  --bind 0.0.0.0:$PORT_APP \
#  --log-level DEBUG \
#  app:app
