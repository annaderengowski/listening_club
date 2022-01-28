# syntax=docker/dockerfile:1
FROM python:3

# set env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

# RUN mkdir -p /code
# WORKDIR /code
# ADD requirements/development.txt /code/
# RUN pip install --upgrade pip wheel setuptools pip-tools
# RUN pip install -r development.txt --no-cache-dir
# RUN apk del .build-dependencies
# ADD . /code/
# WORKDIR /code
# RUN python manage.py collectstatic --no-input
# RUN python manage.py compilemessages
