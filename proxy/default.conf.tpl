server {
    listen ${LISTEN_PORT};
    listen ${HTTPS_LISTEN_PORT} ssl;
    server_name         codesomething.site;
    ssl_certificate /etc/ssl/certs/codesomething.site.crt;
    ssl_certificate_key /etc/ssl/private/codesomething.site.key;


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