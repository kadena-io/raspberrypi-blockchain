#!/usr/bin/env bash

pact -a init.yaml | curl -d @- http://192.168.2.22:8081/api/v1/send
echo