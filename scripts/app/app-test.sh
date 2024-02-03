#!bin/bash

docker-compose -f docker-compose.yml run --rm app \
    sh -c "python manage.py test"
