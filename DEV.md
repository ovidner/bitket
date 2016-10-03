# Install locally
    pip install -r requirements.txt
    
# Run locally with database and redis in Docker

    docker-compose -f compose.yml -f dev.compose.yml up postgres redis
    ./manage.py runserver
