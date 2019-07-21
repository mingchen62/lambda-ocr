
#!/bin/bash

curl -H "X-API-KEY: PNhuKQCO7a1cMsP3stp8EuhaxaNrhtK61UnFS51j" -X POST --data-binary @$1 https://vgiz0u90r3.execute-api.us-east-1.amazonaws.com/beta |jq '.'
