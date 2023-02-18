#!/bin/bash

graph=3
sequ=0

while :
do
        curl -H "Authorization: Token fa1e62b4d81d85a5a23ef6c7523d41a693e8d385" -d "label=&graph=$graph&data=$(( ( RANDOM % 1000 )  + 1 ))&sequence=$sequ" -X POST http://127.0.0.1:8000/api/graphpoints/
        ((sequ=sequ+1))
done
