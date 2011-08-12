#!/usr/bin/env python

"""
Megavideo Link Cleaner (https://github.com/PicciMario/MegaVideo-link-cleaner)
Copyright (c) 2011 PicciMario <mario.piccinelli@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


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
	print("This tool accepts a valid URL and prints a list of all the MegaVideo")
	print("links found in the page (see SCAN MODE later).")
	print("If called with no options it prints just the links found (so this tool")
	print("can be used from another script). Use -d or -v for a more exhaustive")
	print("output.")
	print("")
	print("Usage: mvparse.py -u URL")
	print("")
	print("Other options:")
	print("-h\tThis help")
	print("-d\tDebug info")
	print("-v\tVerbose (still less thank DEBUG)")
	print("-r\tRaw scan mode")
	print("")
	print("SCAN MODE")
	print("0: Default mode. Searches for links in the form") 
	print("   <a href=\"http://www.megavideo.com/?[v/d]=XXXXXXX\">Description</a>")
	print("   and prints an output formatted like:")
	print("     # Description")
	print("     http://www.megavideo.com/?[v/d]=XXXXXXX")
	print("   This mode is useful to create input files for the mvregen tool.")
	print("1: Raw mode. Searches for every occurrence of the regexp")
	print("   http://www.megavideo.com/?[v/d]=XXXXXXX")
	print("")
	print("If you do not use v (verbose) or d (debug), the tool only prints")
	print("out the found url(s) (or the supplied url if this is valid)")
	print("")

newURL = ""
scanMode = 0

try:
	opts, args = getopt.getopt(sys.argv[1:], "hu:vdr")
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
	elif o == "-r":
		scanMode = 1

if (len(newURL) == 0):
	usage()
	print("You need to provide an url.\n")
	sys.exit(0)
	
# -------------------------------------------------------------------------------------------

# tries to get the original file
log.info("Opening page %s"%newURL)
try:
	f = urllib.urlopen(newURL)
	readFile = f.read()
except:
	log.error("Unable to access provided URL (maybe you are offline or misspelled the url?)")
	sys.exit(1)
f.close()

# Raw scan mode
if (scanMode == 1):
	# parses megavideo links
	log.debug("Searching MegaVideo-like links in the downloaded page")
	m = re.findall('http://www.megavideo.com/\?[vd]=[0-9a-zA-Z]{8}', readFile)
	
	# print results
	log.info("Found %i links in the page."%len(m))
	for line in m:
		print line

# Normal scan mode
elif (scanMode == 0):
	# search for generic links
	log.debug("Searching all links in the downloaded page")
	m = re.findall('<a.*?</a>', readFile)
	
	# search megavideo links
	log.debug("Searching MegaVideo Links in the form <a href=\"http://www.megavideo.com/?v/d=XXXXXXXX\">text</a>")
	mvlinks = []
	pattern = re.compile('http://www.megavideo.com/\?[vd]=[0-9a-zA-Z]{8}')
	for line in m:
		if (pattern.search(line) != None):
			mvlinks.append(line)
	
	log.info("Found %i MegaVideo Links in the form <a href=\"http://www.megavideo.com/?v/d=XXXXXXXX\">text</a>"%len(mvlinks))
	
	# parse megavideo links for url and description
	for link in mvlinks:
		
		linkUrl = ""
		linkDesc = ""
		
		linkFound = re.search('(?<=href=")[^"]*', link)
		if (linkFound != None):
			linkUrl = linkFound.group(0)
		
		descFound = re.findall('(?<=>)[^<]*', link)
		for line in descFound:
			if (len(line) > 0):
				linkDesc = line
				continue
		
		print("# %s\n%s"%(linkDesc, linkUrl))