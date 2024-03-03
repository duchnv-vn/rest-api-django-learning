server {
  listen 80;
  server_name codesomething.site www.codesomething.site;
  return 301 https://codesomething.site$request_uri;
}

server {
    listen 443 ssl;

    server_name codesomething.site www.codesomething.site;

    ssl_certificate /ssl/certs/codesomething.site.pem;
    ssl_certificate_key /ssl/private/codesomething.site.key;
    ssl_password_file /ssl/codesomething.site.ssl.pass;

    access_log /var/log/nginx/access.log combined;

    location /static {
      alias /vol/static;
    }

    location / {
      uwsgi_pass               app:9000;
      include                  /etc/nginx/uwsgi_params;
      client_max_body_size     2M;
    }
  }