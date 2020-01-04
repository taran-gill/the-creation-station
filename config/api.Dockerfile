FROM python:3.7.5-stretch

LABEL author=contact@tarangill.dev

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP src/server/entry.py
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

ADD config/setup/sphinx/${SPHINXBASE}.tar.gz   /sphinx/
ADD config/setup/sphinx/${POCKETSPHINX}.tar.gz /sphinx/
ADD config/setup/sphinx/${SPHINXTRAIN}.tar.gz  /sphinx/

RUN mv /sphinx/${SPHINXBASE}   /sphinx/sphinxbase
RUN mv /sphinx/${POCKETSPHINX} /sphinx/pocketsphinx
RUN mv /sphinx/${SPHINXTRAIN}  /sphinx/sphinxtrain

WORKDIR /sphinx/sphinxbase
RUN ./configure --with-swig-python
RUN make 
RUN make install

WORKDIR /sphinx/pocketsphinx
RUN ./configure --with-swig-python
RUN make
RUN make check
RUN make install
RUN make installcheck

WORKDIR /sphinx/sphinxtrain
RUN ./configure
RUN make
RUN make check
RUN make installcheck

ENV SPHINX_MODEL /sphinx/pocketsphinx/model

WORKDIR /api
COPY requirements.txt /api/
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
COPY . /api/

CMD ["python", "src/server/entry.py"]
