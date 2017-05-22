cat metadata.json | jq "[del(.[] | select(.Metadata.Extra.Vav == null)) | .[] | {(.Metadata.Extra.Type): (.uuid), vav: (.Metadata.Extra.Vav)}]"  > vavsensors.json
