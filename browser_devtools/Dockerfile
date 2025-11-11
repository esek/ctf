FROM node:lts-alpine

WORKDIR /usr/app

COPY websockets.js ./

RUN npm init -y
RUN npm install ws

EXPOSE 8080

CMD ["node", "websockets.js"]