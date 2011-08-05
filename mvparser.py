#!/usr/bin/env python

import urllib, string, sys, re, getopt, socket, logging

# ----------- Globals ----------------------------------------------------------------------

# version string
version = "1.0"

# socket default timeout
socket.setdefaulttimeout(20)

# ----------- Logger --------------------------------------------------------------------------------

# Logger
log = logging.getLogger('MV Link Cleaner')
log.setLevel(logging.CRITICAL)
#create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.CRITICAL)
#create formatter
formatter = logging.Formatter("%(levelname)s - %(message)s")
#add formatter to ch
ch.setFormatter(formatter)
#add ch to logger
log.addHandler(ch)

# ----------- Command Line Parameters ---------------------------------------------------------------

def usage():
	print("")
	print("Megavideo URL Parser")
	print("Version %s by PicciMario <mario.piccinelli@gmail.com>"%version)
	print("Released under MIT license. Enjoy!")
	print("")
	print("Usage: mvparse.py -u URL")
	print("")
	print("Other options:")
	print("-d\tDebug info")
	print("-v\tVerbose (still less thank DEBUG)")
	print("")
	print("If you do not use v (verbose) or d (debug), the tool only prints")
	print("out the found url(s) (or the supplied url if this is valid)")
	print("")

newURL = ""

try:
	opts, args = getopt.getopt(sys.argv[1:], "hu:vd")
except getopt.GetoptError:
	usage()
	sys.exit(0)

for o,a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-u":
		newURL = a
		log.info("Supplied %s url from command line"%a)
	elif o == "-v":
		log.setLevel(logging.INFO)
		ch.setLevel(logging.INFO)
	elif o == "-d":
		log.setLevel(logging.DEBUG)
		ch.setLevel(logging.DEBUG)

if (len(newURL) == 0):
	usage()
	print("You need to provide an url.\n")
	sys.exit(0)
	
# -------------------------------------------------------------------------------------------

# tries to get the original file
log.debug("Opening page %s"%newURL)
try:
	f = urllib.urlopen(newURL)
	readFile = f.read()
except:
	log.error("Unable to access provided URL (maybe you are offline or misspelled the url?)")
	sys.exit(1)
f.close()

# parses megavideo links
log.debug("Searching MegaVideo-like links in the downloaded page")
m = re.findall('http://www.megavideo.com/\?[vd]=[0-9a-zA-Z]{8}', readFile)

# print results
log.info("Found %i links in the page."%len(m))
for line in m:
	print line