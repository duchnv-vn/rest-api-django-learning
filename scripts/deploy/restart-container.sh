#!bin/bash
docker-compose -f docker-compose-$ENV-deploy.yml build
docker-compose -f docker-compose-$ENV-deploy.yml up -d