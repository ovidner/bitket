FROM nginx:alpine

RUN mkdir -p /app/build && \
    rm -rf /usr/share/nginx/html/ && \
    ln -s /app/build /usr/share/nginx/html
WORKDIR /app

COPY ./requirements.alpine.txt /app/requirements.alpine.txt
RUN apk add --no-cache $(grep -vE "^\s*#" /app/requirements.alpine.txt | tr "\n" " ") && \
    npm install -g yarn

COPY ./package.json ./yarn.lock /app/
RUN yarn install && \
    yarn cache clean

COPY . /app

ENTRYPOINT ["/app/bin/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
