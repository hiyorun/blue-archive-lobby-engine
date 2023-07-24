#!/bin/bash

paths=$(find models/ -name "*.skel")
items=()
for path in $paths; do
	filename=$(/usr/bin/basename "${path%.skel}")
	name="${filename/_home/""}"
	items+=("{\"name\":\"${name^}\",\"path\":\"$path\"}")
done
itemsToJson=$(IFS=,;echo "${items[*]}")
echo "{\"assets\":[$itemsToJson]}" | jq > src/assets/models.json