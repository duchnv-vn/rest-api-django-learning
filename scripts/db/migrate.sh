#!bin/bash
docker-compose run --rm app \
    sh -c "
        python manage.py wait_for_db && \
        python manage.py migrate
    "
