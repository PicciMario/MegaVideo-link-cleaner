#!/usr/bin/env python

import urllib, string, sys, re, getopt, socket, logging

# ----------- Globals ----------------------------------------------------------------------

# version string
version = "1.0"

# socket default timeout
socket.setdefaulttimeout(20)

# base MegaVideo url string
baseMegavideoUrl = "http://www.megavideo.com/?v="

# output limit
outputLimit = 99

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

# ----------- Checks if the provided URL is an available MegaVideo video -------------------

def checkIfAvailableOnMV(megaVideoUrl):

	log.debug("Checking link %s for existence on MegaVideo"%(megaVideoUrl))
	
	# checks whether the video is not removed from MV
	# 0 -> video available
	# 1 -> removed due to infringement
	# 2 -> video not available
	# -1 -> unable to connect

	#tries to get the original file
	try:
		f = urllib.urlopen(megaVideoUrl)
		readFile = f.read()
	except:
		log.error("Unable to access provided URL (maybe you are offline or misspelled the url?)")
		return -1
	f.close()
	
	#searches for a predefined error string
	errorString = "has been removed due to infringement"
	for line in string.split(readFile, "\n"):
		if string.find(line, errorString) != -1:
			return 1

	#searches for a predefined error string
	errorString = "This video is unavailable"
	for line in string.split(readFile, "\n"):
		if string.find(line, errorString) != -1:
			return 2

	return 0

# ----------- Command Line Parameters ---------------------------------------------------------------

def usage():
	print("")
	print("Megavideo Link Cleaner")
	print("Version %s by PicciMario <mario.piccinelli@gmail.com>"%version)
	print("Released under MIT license. Enjoy!")
	print("")
	print("Usage: regen.py [-u megavideourl | -c megavideocode]")
	print("")
	print("Other options:")
	print("-d\tDebug info")
	print("-v\tVerbose (still less thank DEBUG)")
	print("-l N\tLimit the output to the first N found links (>=1!)")
	print("")
	print("If you supply the megavideocode, the url will be formatted")
	print("as %sXXXXX."%baseMegavideoUrl)
	print("")
	print("If you do not use v (verbose) or d (debug), the tool only prints")
	print("out the found url(s) (or the supplied url if this is valid)")
	print("")

megaVideoUrl = ""

try:
	opts, args = getopt.getopt(sys.argv[1:], "hu:c:vdl:")
except getopt.GetoptError:
	usage()
	sys.exit(0)

for o,a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-u":
		megaVideoUrl = a
		log.info("Supplied %s url from command line"%a)
	elif o == "-c":
		megaVideoUrl = "%s%s"%(baseMegavideoUrl, a)
	elif o == "-v":
		log.setLevel(logging.INFO)
		ch.setLevel(logging.INFO)
	elif o == "-d":
		log.setLevel(logging.DEBUG)
		ch.setLevel(logging.DEBUG)
	elif o == "-l":
		outputLimit = a

if (len(megaVideoUrl) == 0):
	usage()
	print("You need to provide an url or a MegaVideo code.\n")
	sys.exit(0)

try:
	outputLimit = int(outputLimit)
except:
	usage()
	print("If you use the -l option you must provide a valid integer.\n")
	sys.exit(0)

if outputLimit < 1:
	usage()
	print("If you use the -l option you must provide a valid integer >= 1.\n")
	sys.exit(0)	
	
# -------------------------------------------------------------------------------------------

# checks whether the url is available on MegaVideo
availableOnMV = checkIfAvailableOnMV(megaVideoUrl)
if (availableOnMV == -1):
	sys.exit(1)
if (availableOnMV == 1):
	log.info("The original MegaVideo file has been removed due to infringiment")
elif (availableOnMV == 2):
	log.info("The original MegaVideo file is not available")
else:
	log.info("The url: %s is still available on MegaVideo."%megaVideoUrl)
	print("%s"%megaVideoUrl)
	sys.exit(0)

# tries to regen the link via regen.videourls.com
# works only with urls in the form ?v= and not in the new form ?d=

# megavideo code
code = string.rsplit(megaVideoUrl, "=", 1)[1]

# url of the regen page
regenUrls = [
	["regen.megastreaming.org", "http://regen.megastreaming.org/?v="],
	["regen.videourls.com", "http://regen.videourls.com/?v="]
]

# regenerated urls
newUrls = []

for regenUrl in regenUrls:
	completeUrl = "%s%s"%(regenUrl[1], code)
	
	# get the regen page
	log.debug("Opening page %s"%completeUrl)
	try:
		f = urllib.urlopen(completeUrl)
		readFile = f.read()
	except:
		log.warning("Unable to access server %s"%regenUrl[0])
		continue
	f.close()
	
	# checks for error while regenerating
	errorString = "unable to regenerate"
	found = 0
	for line in string.split(readFile, "\n"):
		if string.find(line, errorString) != -1:
			found = 1
			break
	
	if (found == 1):
		log.info("Found nothing with %s"%regenUrl[0])
		continue
	else:
		log.info("Found something with %s"%regenUrl[0])
	
	# parse the regen page
	for line in string.split(readFile, "\n"):
		if string.find(line, "freshlink") != -1:
			m = re.search('<a.*a>', line)
			line = m.group(0)
			m = re.search('>.*<', line)
			line = m.group(0)
			line = line[1:-1]
			log.info("Found %s on %s"%(line, regenUrl[0]))
			newUrls.append(line)

log.info("Found %i alternative links."%len(newUrls))

if (len(newUrls) > outputLimit):
	log.info("Limiting results to first %i value(s) (see -l option)."%outputLimit)

for newLink in newUrls[0:outputLimit]:
	print(newLink)
