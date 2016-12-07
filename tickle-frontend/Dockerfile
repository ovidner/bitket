FROM nginx:alpine

RUN mkdir -p /app/build
WORKDIR /app

COPY ./requirements.alpine.txt /app/requirements.alpine.txt
RUN apk add --no-cache $(grep -vE "^\s*#" /app/requirements.alpine.txt | tr "\n" " ") && \
    npm install -g yarn

COPY ./package.json ./yarn.lock /app/
RUN yarn install && \
    yarn cache clean

COPY . /app
RUN cd /etc/nginx/conf.d && patch default.conf /app/nginx.vh.default.conf.patch

ENTRYPOINT ["/app/bin/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
