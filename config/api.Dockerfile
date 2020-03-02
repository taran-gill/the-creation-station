FROM python:3.7.5-buster

LABEL author=contact@tarangill.dev

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP entry.py
ENV FLASK_ENV development

# System deps
RUN apt-get -qq -y update
RUN apt-get -qq -y install
RUN apt-get -y -qq install ffmpeg

WORKDIR /api
COPY requirements.txt /api/
RUN pip install -r requirements.txt
COPY . /api/

RUN python setup.py install --user

CMD ["python", "entry.py"]
