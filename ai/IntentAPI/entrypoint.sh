#!/bin/sh
while ! (nc -z text2vec 3303); do
  sleep 0.1
  echo "Waiting for text2vec to start"
done
exec "$@"