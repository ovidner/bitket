FROM nginx:alpine

RUN mkdir -p /app/build
WORKDIR /app

# Installs APK packages. Yarn is not available as an APK package (yet) and is
# installed manually
COPY ./requirements.alpine.txt /app/requirements.alpine.txt
RUN apk add --no-cache $(grep -vE "^\s*#" /app/requirements.alpine.txt | tr "\n" " ") && \
    mkdir -p /opt/yarn && \
    curl -o- -L https://yarnpkg.com/latest.tar.gz | tar -zxC /opt/yarn && \
    ln -s /opt/yarn/dist/bin/yarn /usr/bin/yarn

COPY ./package.json ./yarn.lock /app/
RUN yarn install && \
    yarn cache clean

COPY . /app
RUN cd /etc/nginx/conf.d && patch default.conf /app/nginx.vh.default.conf.patch

ENTRYPOINT ["/app/bin/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
