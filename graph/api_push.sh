#!/bin/bash

graph=2
data=$1
curl -H "Authorization: Token e49d33d3db99d484e9d4a14a142d547db720903d" -d "label=t&graph=$graph&data=$data" -X POST http://localhost:8080/graphs/api/graphpoints/
