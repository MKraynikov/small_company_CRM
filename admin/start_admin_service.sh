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
python manage.py loaddata apps/account/fixtures/user_status_ru.json
python manage.py compilemessages -l en -l ru
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@admin.local', 'admin')"

exec "$@"
