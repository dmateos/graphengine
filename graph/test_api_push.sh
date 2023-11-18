#!/bin/bash

graph=1

while :
do
        curl -H "Authorization: Token e49d33d3db99d484e9d4a14a142d547db720903d" -d "label=t&graph=$graph&data=$(( ( RANDOM % 1000 )  + 1 ))" -X POST http://localhost:8080/graphs/api/graphpoints/
        sleep 1
done
