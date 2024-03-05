FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="huynhnguyenvietduc@gmail.com"

COPY ./nginx.conf.tpl /etc/nginx/nginx.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV APP_HOST=app
ENV APP_PORT=9000
ENV SERVER_NAME=codesomething.site
ENV SSL_CERT_FILE_PATH=/ssl/certs/codesomething.site.pem
ENV SSL_CERT_PRIVATE_KEY_FILE_PATH=/ssl/private/codesomething.site.key
ENV SSL_CERT_PASSWORD_FILE_PATH=/ssl/codesomething.site.ssl.pass

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD [ "/run.sh" ]