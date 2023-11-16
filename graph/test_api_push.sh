#!/bin/bash

graph=1
sequ=0

while :
do
        curl -H "Authorization: Token e49d33d3db99d484e9d4a14a142d547db720903d" -d "label=&graph=$graph&data=$(( ( RANDOM % 1000 )  + 1 ))&sequence=$sequ" -X POST http://127.0.0.1:8080/graphs/api/graphpoints/
        ((sequ=sequ+1))
done
