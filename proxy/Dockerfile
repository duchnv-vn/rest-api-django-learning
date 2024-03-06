FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="huynhnguyenvietduc@gmail.com"


COPY ./nginx.conf.tpl /etc/nginx/nginx.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV APP_HOST=app
ENV APP_PORT=9000
ENV DOMAIN_NAME=codesomething.site
ENV SSL_CERT_FILE_PATH=/letsencrypt/live/codesomething.site/fullchain.pem
ENV SSL_CERT_PRIVATE_KEY_FILE_PATH=/letsencrypt/live/codesomething.site/privkey.pem

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD [ "/run.sh" ]