Holiday hacks
=============

Python scripts to drive a set of Holiday LED lights using the Secret API.

See https://github.com/moorescloud/secretapi for the Python library (holidaysecretapi.py)

For these to work, your Holiday needs to be on your local wifi, and its IP address should be passed to the script as a command-line argument. eg:

  chaser.py 10.1.1.9


## chaser.py

Basic colour-pattern chaser

## cellular/carunner.py

New-ish and badly documented and factored scripts for 1-D cellular automata.
Run cellular/carunner.py 

## drops.py

Flashes of colour

## sines.py

Adds a red, green and blue waveform to give a pleasant, ever-changing, never-quite-repeating rainbow

## sort.py

The nerdiest lights - visualisations of four different sort algorithms
operating on randomly-generated and shuffled colour gradients

## what_colour_is_it.py

Displays the current time as a hex-colour triplet, after
[this website](http://whatcolourisit.scn9a.org/)

## sniffy.py

VERY BETA and naive network activity visualiser.  This requires the
pycapy and impacket packet sniffing libraries, has to be run as root,
ignores IP6 packets and should not be used by anyone.

## pulse.py

Provides two classes, Pulse (a string of colours with velocity and
position) and Pulser (a Thread which accepts new Pulses on a queue and
animates them on the lights).

This is used to visualise packets in sniffy.py but is intended to be a
general-purpose-visualise-things-as-pulses tool.

If it's run from the command line like the other scripts, goes into a
test mode which generates random pulses.

