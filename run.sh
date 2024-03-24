#!/bin/shell

export BOT_TOKEN=
export DATABASE_URL=
export DATABASE_NAME=
export NOTIFICATION_RECIEPENT_ID=
export NOTIFIER_TOKEN=
export ADMIN_USERS=
export SUPER_USER=

python __main__.py 2 >>main.log >&1 &

echo "Started running the bot in the background"
