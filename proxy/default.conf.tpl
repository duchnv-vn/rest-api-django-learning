server {
    listen ${LISTEN_PORT};

    location /.well-known/acme-challenge {
        alias /vol/static/static;
    }

    location /static {
        alias /vol/static;
    }

    location / {
        uwsgi_pass               ${APP_HOST}:${APP_PORT};
        include                  /etc/nginx/uwsgi_params;
        client_max_body_size     2M;
    }
}

server {
    listen ${HTTPS_LISTEN_PORT} ssl;

    location /.well-known/acme-challenge {
        alias /vol/static/static;
    }

    location /static {
        alias /vol/static;
    }

    location / {
        uwsgi_pass               ${APP_HOST}:${APP_PORT};
        include                  /etc/nginx/uwsgi_params;
        client_max_body_size     2M;
    }
}