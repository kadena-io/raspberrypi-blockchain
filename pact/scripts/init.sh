#!/usr/bin/env bash

pact -a init.yaml | curl -d @- http://localhost:8081/api/v1/send
echo