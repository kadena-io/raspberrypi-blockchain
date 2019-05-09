#!/usr/bin/env bash

# create "log" directory if does not exists
if [ ! -d "log" ]; then
	mkdir log
fi

pact -s config.yaml
