#!/bin/bash

SOURCE=${1:-'models/'}
DESTINATION=${2:-'src/assets/models.json'}

paths=$(find $SOURCE -name "*.skel")
items=()
for path in $paths; do
	filename=$(/usr/bin/basename "${path%.skel}")
	name="${filename/_home/""}"
	items+=("{\"name\":\"${name^}\",\"path\":\"$path\"}")
done
itemsToJson=$(IFS=,;echo "${items[*]}")
echo "{\"assets\":[$itemsToJson]}" | jq > $DESTINATION