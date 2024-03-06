#!bin/bash
sudo docker-compose -f docker-compose-$ENV-deploy.yml \
  run --rm certbot renew \
  --nginx --standalone --preferred-challenges http \
  -d $DOMAIN_NAME
