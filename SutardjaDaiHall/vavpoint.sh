#!/bin/bash 

smap-query -u http://new.openbms.org:8079/api/query "select Metadata/Extra/Type, uuid where Metadata/Extra/Vav = '${1}' and has Metadata/Extra/Type" > x.json

tail -n +2 x.json | jq ".[] | {(.Metadata.Extra.Type): .uuid} " | jq -s add
