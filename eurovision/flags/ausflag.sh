#!/bin/bash


for svg in "$@"
do
    bn=$(basename "$svg")
    file="${bn%.*}"
    echo "$svg -> $file"
    convert -resize 600x300! "$bn" "$file.png"
    composite "$file.png" Ausback.png "au_$file.png"
done

montage -tile 5x8 -geometry 100x50+8+8 au_Flag_of_*.png final.png
