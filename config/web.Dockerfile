FROM node:8.16.2-buster

WORKDIR /web

RUN mkdir -p /node_modules/.bin

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin

RUN yarn global add react-scripts@3.0.1

COPY . .

CMD /bin/bash -c 'yarn --no-bin-links; yarn start'
