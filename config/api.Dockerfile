FROM python:3.7.5-buster

LABEL author=contact@tarangill.dev

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP entry.py
ENV FLASK_ENV development

# System deps
RUN apt-get -qq -y update
RUN apt-get -qq -y install
RUN apt-get -qq -y install build-essential && \
    apt-get -qq -y install swig libpulse-dev portaudio19-dev && \
    apt-get -qq -y install sox bison && \
    apt-get -y -qq install ffmpeg

ENV SPHINXBASE   sphinxbase-5prealpha
ENV POCKETSPHINX pocketsphinx-5prealpha
ENV SPHINXTRAIN  sphinxtrain-5prealpha

ADD ./packages/detect_filler_words/config/setup/sphinx/${SPHINXBASE}.tar.gz   /sphinx/
ADD ./packages/detect_filler_words/config/setup/sphinx/${POCKETSPHINX}.tar.gz /sphinx/
ADD ./packages/detect_filler_words/config/setup/sphinx/${SPHINXTRAIN}.tar.gz  /sphinx/

RUN mv /sphinx/${SPHINXBASE} /sphinx/sphinxbase && \
    mv /sphinx/${POCKETSPHINX} /sphinx/pocketsphinx && \
    mv /sphinx/${SPHINXTRAIN} /sphinx/sphinxtrain

WORKDIR /sphinx/sphinxbase
RUN ./configure --with-swig-python
RUN make && make check && make install && make installcheck

WORKDIR /sphinx/pocketsphinx
RUN ./configure --with-swig-python
RUN make && make check && make install && make installcheck

WORKDIR /sphinx/sphinxtrain
RUN ./configure
RUN make && make check && make installcheck

WORKDIR /api
COPY requirements.txt /api/
RUN pip install -r requirements.txt
COPY . /api/

ENV PYTHONPATH /usr/local/lib/python3.4/site-packages

RUN python setup.py install --user

CMD ["python", "entry.py"]
