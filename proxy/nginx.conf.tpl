events { }

http {
  map $http_upgrade $connection_upgrade {
      default upgrade;
      ''      close;
  }

  server {
    listen ${LISTEN_PORT};
    server_name ${SERVER_NAMES};
    return 301 https://${SERVER_NAME}$request_uri;
  }

   server {
    listen ${HTTPS_LISTEN_PORT} ssl;
    server_name ${SERVER_NAMES};

    ssl_certificate /etc/ssl/certs/codesomething.site.pem;
    ssl_certificate_key /etc/ssl/private/codesomething.site.key;

    access_log /var/log/nginx/data-access.log combined;

    location /static {
      alias /vol/static;
    }

    location / {
      uwsgi_pass               ${APP_HOST}:${APP_PORT};
      include                  /etc/nginx/uwsgi_params;
      client_max_body_size     2M;
    }
   }
}