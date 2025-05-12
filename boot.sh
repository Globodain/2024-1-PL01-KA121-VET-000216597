#!/bin/bash
source venv/bin/activate

flask db upgrade
flask translate compile

if [ "$FLASK_ENV" = "development" ]; then
    exec flask run --host=0.0.0.0 --port=5000 --reload
else
    exec gunicorn -b :5000 --access-logfile - --error-logfile - "microblog:create_app()"
fi