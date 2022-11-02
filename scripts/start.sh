#!/bin/bash

export $(grep -v '^#' .env | xargs) >> /dev/null 2>&1 

if [ -z ${LNBITS_MAIN_WALLET_ADMIN_KEY+x} ]; then
    LNBITS_URL=$(echo $LNBITS_HOST | awk '{gsub("/api",""); print}')"/wallet?nme=default"
    LNBITS_URL=$(echo $LNBITS_URL | awk '{gsub("host.docker.internal","127.0.0.1"); print}')
    LNBITS_WALLET_URL=$(curl -X GET --head --silent --write-out "%{redirect_url}\n" --output /dev/null $LNBITS_URL)
    LNBITS_WALLET_SOURCE=$(curl -L -s -w "\n%{http_code}" "${LNBITS_WALLET_URL}")
    LNBITS_WALLET_KEYS=$(echo $LNBITS_WALLET_SOURCE | python3 -c 'import sys, json, re; print(re.search(r"window\.wallet = ({.*});", sys.stdin.read()).group(1))')

    LNBITS_MAIN_WALLET_ADMIN_KEY=$(echo $LNBITS_WALLET_KEYS | jq .adminkey) 
    LNBITS_MAIN_WALLET_INVOICE_KEY=$(echo $LNBITS_WALLET_KEYS | jq .inkey)

    echo $LNBITS_WALLET_URL > ./lnbits.url
    echo "" >> .env
    echo "LNBITS_MAIN_WALLET_ADMIN_KEY=${LNBITS_MAIN_WALLET_ADMIN_KEY}" >> .env
    echo "LNBITS_MAIN_WALLET_INVOICE_KEY=${LNBITS_MAIN_WALLET_INVOICE_KEY}" >> .env
fi

docker-compose --env-file .env up -d