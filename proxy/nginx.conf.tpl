events {}

server {
    listen 80;
    listen 443 ssl;
    if ($scheme = http) {
      return 301 https://codesomething.site$request_uri;
    }

    server_name codesomething.site www.codesomething.site;

    ssl_certificate /etc/ssl/certs/codesomething.site.pem;
    ssl_certificate_key /etc/ssl/private/codesomething.site.key;

    access_log /var/log/nginx/data-access.log combined;

    location /static {
      alias /vol/static;
    }

    location / {
      uwsgi_pass               app:9000;
      include                  /etc/nginx/uwsgi_params;
      client_max_body_size     2M;
    }
  }