cat metadata.json | jq "[del(.[] | select(.Metadata.Extra.Vav == null)) | .[] | {(.Metadata.Extra.Type): (.uuid), PointName: (.Metadata.PointName), vav: (.Metadata.Extra.Vav)}]"  > vavsensors.json
