#!/bin/bash

if [[ ! -f $VIRTUAL_ENV/bin/python ]];
then
    echo "Creating virtualenv"
    virtualenv $VIRTUAL_ENV
fi

if [[ "$ENV" = "PROD" ]] || [[ "$ENV" = "DEMO" ]] || [[ "$ENV" = "STAGE" ]] || [[ "$ENV" = "DEV" ]];
then
    echo "Not running in a docker-compose environment, skipping wait-for-it"

    echo "Loading AWS CLI virtualenv"
    source /opt/aws/bin/activate

    /download-certs.sh

    echo "Deactivating AWS CLI virtualenv"
    deactivate

    exec "$@"
else
    echo "Waiting for dependencies to come up in the stack"
    /wait-for-it.sh ${REDIS_NAME:-redis_db}:6379
    /wait-for-it.sh ${PSQL_NAME:-psql}:5432
    /wait-for-it.sh ${MINIO_NAME:-minio}:9000

    if [[ -z "$IS_DDO" ]];
    then
        python manage.py migrate
    fi
    USER_ID=${LOCAL_USER_ID:0}
    GROUP_ID=${LOCAL_GROUP_ID:0}
    echo "Starting with GUID:UID : $GROUP_ID:$USER_ID"
    addgroup -g $GROUP_ID -S username && adduser -u $USER_ID -S username -G username
    exec su-exec $USER_ID:$GROUP_ID "$@"
fi
