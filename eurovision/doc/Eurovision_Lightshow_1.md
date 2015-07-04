Eurovision Lightshow 1
======================

This is the first of three blog posts detailing an incredibly daggy
project: setting up a string of programmable LED lights as a lightshow
for my Eurovision housewarming party, using a Raspberry Pi as the
controller.  The most generally useful part of it is the second post,
which is about how easy it is to whip up a well-behaved customised
server for a Unix system using the Python event-based programming
framework Twisted.

## National Colours

I got one of the last sets of Holiday lights, a really nice string of
50 programmable LEDs produced by an Australian startup.  Holidays have
a wifi connection and can be controlled with a simple API, which sends
a set of 50 RGB values to update the lights.  I'd already done a bunch
of scripts to animate the lights in Python - a language I know
moderately well, which I selected because the example code used it.

The first idea I had for the Eurovision lights was a simple chaser
pattern in the national colours of each of the entrants. I already had
RGB values for these from making the image below for the party invite:

![Australian flags of all nations](https://raw.githubusercontent.com/spikelynch/holiday/master/eurovision/doc/AusEuro.png "Australia")

Wikipedia has [SVG files for national
flags,](https://en.wikipedia.org/wiki/Flag_of_Australia#/media/File:Flag_of_Australia.svg).
To make the above image, I'd written a script to download the 40 SVG
files, and then another script using ImageMagick, a venerable set of
image manipulation tools, to render the SVGs at the right size and
plonk them on an Australian flag in place of the Union Jack.

    for svg in "$@"
    do
        bn=$(basename "$svg")
        file="${bn%.*}"
        echo "$svg -> $file"
        convert -resize 600x300! "$bn" "$file.png"
        composite "$file.png" Ausback.png "au_$file.png"
    done

    montage -tile 5x8 -geometry 100x50+8+8 au_Flag_of_*.png final.png


## Flags Are Weird: A Digression

What's the aspect ratio of a flag? 2:1 seemed like a good guess, I
thought, unless it's 4:3, like an old movie screen? Or... 13:15?  Go
home, Belgian national flag, you're drunk:

https://en.wikipedia.org/wiki/List_of_countries_by_proportions_of_national_flags

I ended up forcing everything to be 2:1.

Two other things are worth noting about this part of the process:
ImageMagick kept crashing when it got to Portugal.  This turns out to
be a problem with ImageMagick's native SVG parser, which barfs if you
give it something too complex.  On a Mac, installing ImageMagick with
the librsvg library fixed this:

    brew install ImageMagick --with-librsvg librsvg

The other thing is that SVG file size gives us a way to order national flags in order of Fanciness:

![Screenshot of a directory listing of SVG files](https://raw.githubusercontent.com/spikelynch/holiday/master/eurovision/doc/Fanciness.png "Fanciness")

## The Worst Display In The World

I revisited the SVG files with the idea of stripping RGB values out of
them for my chaser lights, but it struck me that I could try rendering
not just the colours but the flag design, if I arrangeed the Holiday
to form a 10x5 grid, AKA the worst display in the world:

[ photo of the unlit grid ]

For this to work, I'd need to get 10x5 renderings of the SVG files,
and adapt my existing Python scripts to render the colours to the
lights in the right order.

ImageMagick can write out just about anything, so I used PPM, an old
Unix format which I picked because it's basically a text file of pixel
values and thus easy to reprocess into other formats.

Once I had the bitmaps, I made another little Perl script to convert
them into Python code, and adapted one of my existing Holiday scripts
to render them to the lights.  The problem was: with the exception of
tricolors, almost all national flags look like unrecognisable blurs at
10x5:

![Chunky pixels](https://raw.githubusercontent.com/spikelynch/holiday/master/eurovision/doc/PixelFlag.png "Chunky!")

[ lit-up Holiday]

Part two will be about how I animated the flag patterns to give them a
bit of life and also make them recognisable, and how I built a
mini-server to control them from my Raspberry Pi.
