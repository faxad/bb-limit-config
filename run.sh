#!/bin/bash

[[ $1 == "build" ]] && docker build . -t bb-limit:1.0

docker run -v ./payload:/usr/app/src/payload -t bb-limit:1.0


ENDPOINT="https://postman-echo.com/post"
BASE_REQUEST_PATH="./payload/request"
BASE_RESPONSE_PATH="./payload/response"

for filename in $BASE_REQUEST_PATH/*.json; do
    file=$(basename "$filename")

    echo $file

    HTTP_RESPONSE=$(curl --silent --write-out "HTTPSTATUS:%{http_code}" -X POST -H "Content-Type: application/json" -d @$filename $ENDPOINT)
    HTTP_BODY=$(echo $HTTP_RESPONSE | sed -e 's/HTTPSTATUS\:.*//g')
    HTTP_STATUS=$(echo $HTTP_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

    if [ $HTTP_STATUS -eq 200  ]; then
        SUB="success"
    else
        SUB="failure"
    fi

    echo $HTTP_BODY > $BASE_RESPONSE_PATH/$SUB/$file
    sleep 3
done