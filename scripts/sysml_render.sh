#!/bin/sh
# usage: render.sh file.puml -> SVG and PNG next to it (the PNG is 700 px wide by `scale 700 width` in the text)
set -e
f=$1; b=${f%.*}
plantuml -Djava.awt.headless=true -tsvg "$f"
plantuml -Djava.awt.headless=true -tpng "$f"
sips -g pixelWidth -g pixelHeight "$b.png" | tail -2 | tr '\n' ' '; echo
