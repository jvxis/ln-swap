FROM node:16.16.0-alpine
WORKDIR /app
COPY package.json /app
COPY package-lock.json /app
COPY . /app
COPY scripts /app
RUN npm i
EXPOSE 5173
CMD [ "sh", "/app/scripts/start.sh" ]