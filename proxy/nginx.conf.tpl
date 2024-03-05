server {
  listen 80;
  listen [::]:80;
  server_name ${SERVER_NAME} www.${SERVER_NAME};
  server_tokens off;

  location /.well-known/acme-challenge/ {
      root /var/www/certbot;
  }

  location / {
    return 301 https://${SERVER_NAME}$request_uri;
  }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name ${SERVER_NAME} www.${SERVER_NAME};

    ssl_certificate ${SSL_CERT_FILE_PATH};
    ssl_certificate_key ${SSL_CERT_PRIVATE_KEY_FILE_PATH};
    ssl_password_file ${SSL_CERT_PASSWORD_FILE_PATH};

    location /static {
      alias /vol/static;
    }

    location / {
      uwsgi_pass               ${APP_HOST}:${APP_PORT};
      include                  /etc/nginx/uwsgi_params;
      client_max_body_size     2M;
    }
  }