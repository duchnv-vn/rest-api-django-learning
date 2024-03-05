server {
  listen 80;
  listen [::]:80;
  server_name ${DOMAIN_NAME} www.${DOMAIN_NAME};
  server_tokens off;

  location /.well-known/acme-challenge/ {
      root /var/www/certbot;
  }

  location / {
    return 301 https://${DOMAIN_NAME}$request_uri;
  }
}

server {
    listen 443 default_server ssl http2;
    listen [::]:443 ssl http2;

    server_name ${DOMAIN_NAME} www.${DOMAIN_NAME};

    ssl_certificate ${SSL_CERT_FILE_PATH};
    ssl_certificate_key ${SSL_CERT_PRIVATE_KEY_FILE_PATH};

    location /static {
      alias /vol/static;
    }

    location / {
      proxy_pass               http://${DOMAIN_NAME};
      uwsgi_pass               ${APP_HOST}:${APP_PORT};
      include                  /etc/nginx/uwsgi_params;
      client_max_body_size     2M;
    }
  }