FROM node:8.16.2-buster

WORKDIR /web
VOLUME /web

RUN mkdir -p src/client/node_modules/.bin

ENV NODE_PATH=src/client/node_modules
ENV PATH=$PATH:src/client/node_modules/.bin

RUN yarn global add react-scripts@3.0.1

COPY src/client/ .

CMD /bin/bash -c 'yarn --no-bin-links; yarn start'
