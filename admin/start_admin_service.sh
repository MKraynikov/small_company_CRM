#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Postgres not run..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "Postgres correctly started."
fi

python manage.py migrate
python manage.py collectstatic --no-input --clear
python3 manage.py loaddata apps/account/fixtures/user_status.json
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.local', 'admin')"

exec "$@"
