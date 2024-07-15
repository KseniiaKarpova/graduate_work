#!/bin/sh
poetry run alembic upgrade head
poetry run python3 cli_create_super_user.py $ADMIN_LOGIN $ADMIN_PASSWORD $ADMIN_EMAIL
echo $ADMIN_PASSWORD asdasd
exec "$@"