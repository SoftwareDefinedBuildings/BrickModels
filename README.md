# Brick Models

There are two Brick files for each building, and one 'generation' script
* `generate_<name>.py`: assembles the Turtle file using any additional sources in the folder
* `name.ttl`: the generated Turtle file
* `name-withinverse.ttl`: the generated Turtle file with all inverse edges added

Also we have `fillout.py` which adds the inverse edges
