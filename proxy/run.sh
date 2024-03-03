#!/bin/sh

set -e

# envsubst </etc/nginx/default.conf.tpl >/etc/nginx/conf.d/default.conf
envsubst </etc/nginx/nginx.conf.tpl >/etc/nginx/sites-available/default.conf

nginx -g 'daemon off;'
