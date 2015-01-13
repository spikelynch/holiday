Holiday hacks
=============

Python scripts to drive a set of Holiday LED lights using the Secret API.

See https://github.com/moorescloud/secretapi for the Python library (holidaysecretapi.py)

Scripts:

* chaser.py - Basic colour-pattern chaser
* drops.py - Flashes of colour
* sines.py - Adds a red, green and blue waveform to give a pleasant, ever-changing, never-quite-repeating rainbow
* quicksort.py - The nerdiest lights! A visualisation of the quicksort algorithm
* what_colour_is_it.py - Displays the current time as a hex-colour triplet, after [this website](http://whatcolourisit.scn9a.org/)
* sniffy.py - VERY BETA and naive network activity visualiser.  This requires the pycapy and impacket packet sniffing libraries, has to be run as root and should not be used by anyone.
* pulse.py - A general-purpose module which runs its own thread to visualise things which are fed into a queue as pulses. Used by sniffy.py, but if it's run on its own it does a nice random set of pulses.

For these to work, your Holiday needs to be on your local wifi, and its IP address should be passed to the script as a command-line argument. eg:

  chaser.py 10.1.1.9

