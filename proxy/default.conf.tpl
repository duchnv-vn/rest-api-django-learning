worker_processes 1;

events { worker_connections 1024; }

http {
    sendfile on;
    large_client_header_buffers 4 32k;

    server {
        listen ${LISTEN_PORT};

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen ${HTTPS_LISTEN_PORT} ssl;
        server_name         codesomething.site;
        ssl_certificate /etc/ssl/certs/codesomething.site.crt;
        ssl_certificate_key /etc/ssl/private/codesomething.site.key;

        location /static {
            alias /vol/static;
        }

        location / {
            proxy_pass         0.0.0.0:8080;
            proxy_redirect     off;
            proxy_http_version 1.1;
            proxy_cache_bypass $http_upgrade;
            proxy_set_header   Upgrade $http_upgrade;
            proxy_set_header   Connection keep-alive;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Proto $scheme;
            proxy_set_header   X-Forwarded-Host $server_name;
            proxy_buffer_size           128k;
            proxy_buffers               4 256k;
            proxy_busy_buffers_size     256k;
        }
    }
}