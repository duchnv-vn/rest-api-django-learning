#!bin/bash
sudo docker-compose -f docker-compose-$ENV-deploy.yml \
  run --rm certbot run \
  --nginx --standalone --preferred-challenges http \
  -d $DOMAIN_NAME
