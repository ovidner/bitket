FROM alpine:3.6

# PIP_NO_CACHE_DIR=false actually means *no cache*
ENV APP_ROOT=/app \
    DJANGO_SETTINGS_MODULE=bitket.settings \
    PIP_NO_CACHE_DIR=false \
    PIPENV_DONT_LOAD_ENV=true \
    PYTHONUNBUFFERED=true

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

COPY apk-packages.txt ${APP_ROOT}/
RUN apk add --no-cache $(grep -vE "^\s*#" ${APP_ROOT}/apk-packages.txt | tr "\r\n" " ") && \
    pip3 install -U pip pipenv setuptools wheel

COPY Pipfile Pipfile.lock ${APP_ROOT}/
RUN pipenv install --system --deploy

COPY package.json yarn.lock ${APP_ROOT}/
RUN yarn install && yarn cache clean

COPY . ${APP_ROOT}/

RUN pip3 install -e ${APP_ROOT} && \
    yarn build && \
    BITKET_DATABASE_URL=sqlite://// BITKET_EMAIL_URL=consolemail:// BITKET_REDIS_URL=redis:// BITKET_SECRET_KEY=build django-admin collectstatic --no-input

EXPOSE 80
