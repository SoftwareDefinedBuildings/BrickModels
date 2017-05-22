cat metadata.json | jq '.[] | select(.Metadata.PointName !=null) | select(.Path | contains("RHC")) | {(.Metadata.PointName): .uuid} ' | jq -s add > rhc_point.json
