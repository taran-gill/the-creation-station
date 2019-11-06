FROM python:3.8.0-buster

LABEL author=contact@tarangill.dev

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP src/server/entry.py
ENV FLASK_ENV development

# System deps
RUN apt-get -qq -y update
RUN apt-get -qq -y install
RUN apt-get -y -qq install ffmpeg

RUN mkdir /project
WORKDIR /project
COPY requirements.txt /project/
RUN pip install -r requirements.txt
COPY . /project/

CMD ["python", "src/server/entry.py"]
