#! /bin/bash
set -e

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

worker=${WORKER:-1}
port=${DJANGO_PORT:-8080}


python scripts/collect_static.py
python manage.py migrate
python manage.py loaddata scripts/fixtures/*

echo "PRODUCTION is: $PRODUCTION"

if [ "$PRODUCTION" == "TRUE" ]; then
  gunicorn --bind 0.0.0.0:${port} -k gevent -w ${worker} project.wsgi
else
  python manage.py runserver 0.0.0.0:${port}
fi
