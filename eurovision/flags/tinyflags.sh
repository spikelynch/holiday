#!/bin/bash

# renders the SVG flags as 10x5 PPMs with compression off so that they can
# be converted into colors for the Holiday lights

for svg in "$@"
do
    bn=$(basename "$svg")
    file="${bn%.*}"
    echo "$svg"
    if [ ! -d "$file" ]; then
        mkdir "$file"
    fi
    convert -resize 10x5! -depth 8 -compress none "../$bn" "$file/10.ppm"
    convert -resize 12x6! -depth 8 -compress none "../$bn" "$file/12.ppm"
    convert -resize 14x7! -depth 8 -compress none "../$bn" "$file/14.ppm"
    convert -resize 16x8! -depth 8 -compress none "../$bn" "$file/16.ppm"
    convert -resize 18x9! -depth 8 -compress none "../$bn" "$file/18.ppm"
    convert -resize 20x10! -depth 8 -compress none "../$bn" "$file/20.ppm"
    convert -resize 22x11! -depth 8 -compress none "../$bn" "$file/14.ppm"
    convert -resize 24x12! -depth 8 -compress none "../$bn" "$file/16.ppm"
    convert -resize 30x15! -depth 8 -compress none "../$bn" "$file/30.ppm"
    convert -resize 40x20! -depth 8 -compress none "../$bn" "$file/40.ppm"
done
