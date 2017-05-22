cat metadata.json | jq '[.[] | select(.Metadata.PointName !=null) | select(.Path | contains("RAH")) | {(.Metadata.PointName): .uuid, Description: (.Description)}]' >rah_points.json
