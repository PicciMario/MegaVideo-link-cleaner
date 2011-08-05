#!/usr/bin/env python

import urllib, string, sys, re, getopt, socket

# ----------- Globals ----------------------------------------------------------------------

# version string
version = "1.0"

# socket default timeout
socket.setdefaulttimeout(20)

# base MegaVideo url string
baseMegavideoUrl = "http://www.megavideo.com/?v="

# ----------- Checks if the provided URL is an available MegaVideo video -------------------

def checkIfAvailableOnMV(megaVideoUrl):
	
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
		print("Unable to access MegaVideo server (maybe you are offline?)")
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
	print("If you supply the megavideocode, the url will be formatted")
	print("as %sXXXXX."%baseMegavideoUrl)
	print("")

megaVideoUrl = ""

try:
	opts, args = getopt.getopt(sys.argv[1:], "hu:c:")
except getopt.GetoptError:
	usage()
	sys.exit(0)

for o,a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-u":
		megaVideoUrl = a
	elif o == "-c":
		megaVideoUrl = "%s%s"%(baseMegavideoUrl, a)

if (len(megaVideoUrl) == 0):
	usage()
	print("You need to provide an url or a MegaVideo code.\n")
	sys.exit(0)

# -------------------------------------------------------------------------------------------

# checks whether the url is available on MegaVideo
availableOnMV = checkIfAvailableOnMV(megaVideoUrl)
if (availableOnMV == -1):
	sys.exit(1)
if (availableOnMV == 1):
	print("The original MegaVideo file has been removed due to infringiment")
elif (availableOnMV == 2):
	print("The original MegaVideo file is not available")
else:
	print("The url:\n-> %s\nis still available.\n"%megaVideoUrl)
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
	try:
		f = urllib.urlopen(completeUrl)
		readFile = f.read()
	except:
		print("Unable to access server %s"%regenUrl[0])
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
		print("Found nothing with %s"%regenUrl[0])
		continue
	else:
		print("Found something with %s"%regenUrl[0])
	
	# parse the regen page
	for line in string.split(readFile, "\n"):
		if string.find(line, "freshlink") != -1:
			m = re.search('<a.*a>', line)
			line = m.group(0)
			m = re.search('>.*<', line)
			line = m.group(0)
			line = line[1:-1]
			print("-> %s"%line)
			newUrls.append(line)

#print(newUrls)
