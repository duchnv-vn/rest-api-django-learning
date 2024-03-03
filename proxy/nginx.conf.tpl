events {}

http {
  map $http_upgrade $connection_upgrade {
      default upgrade;
      ''      close;
  }

  server {
    listen 80;
    server_name codesomething.site www.codesomething.site;
    return 301 https://codesomething.site$request_uri;
  }

  server {
    listen 443 ssl;
    server_name codesomething.site www.codesomething.site;

    ssl_certificate /etc/ssl/certs/codesomething.site.pem;
    ssl_certificate_key /etc/ssl/private/codesomething.site.key;

    access_log /var/log/nginx/data-access.log combined;

    location /static {
      alias /vol/static;
    }

    location / {
      proxy_pass http://app:80/;
      proxy_set_header X-Real-IP  $remote_addr;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_redirect http://app:80/ $scheme://$http_host/;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection $connection_upgrade;
      proxy_read_timeout 20d;
      proxy_buffering off;
    }
  }
}