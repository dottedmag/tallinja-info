#!/bin/sh

D=$(date +%F_%T)

curl -s -H 'x-api-version: 1.3.1' \
  https://www.publictransport.com.mt/appws/StopsMap/GetBusStops \
  -d '' \
  > $HOME/busstops/busstops-$D.json
