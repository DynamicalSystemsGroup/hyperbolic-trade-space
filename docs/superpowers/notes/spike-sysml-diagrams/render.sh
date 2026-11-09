#!/bin/sh
# usage: render.sh file.puml|file.dot -> SVG, full PNG, 700 px and 375 px PNGs next to it
set -e
f=$1; b=${f%.*}
case $f in
 *.puml) plantuml -Djava.awt.headless=true -tsvg "$f"; plantuml -Djava.awt.headless=true -tpng "$f";;
 *.dot) dot -Tsvg "$f" -o "$b.svg"; dot -Tpng -Gdpi=200 "$f" -o "$b.png";;
esac
sips --resampleWidth 700 "$b.png" --out "${b}_700.png" >/dev/null
sips --resampleWidth 375 "$b.png" --out "${b}_375.png" >/dev/null
sips -g pixelWidth -g pixelHeight "$b.png" | tail -2 | tr '\n' ' '; echo
