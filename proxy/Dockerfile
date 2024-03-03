FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="huynhnguyenvietduc@gmail.com"

# COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./nginx.conf.tpl /etc/nginx/nginx.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=80
ENV HTTPS_LISTEN_PORT=443
ENV APP_HOST=app
ENV APP_PORT=9000
ENV SERVER_NAME=codesomething.site
ENV SERVER_NAMES="$SERVER_NAME www.$SERVER_NAME"

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    # touch /etc/nginx/conf.d/default.conf && \
    # chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    touch /etc/nginx/nginx.conf && \
    chown nginx:nginx /etc/nginx/nginx.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD [ "/run.sh" ]