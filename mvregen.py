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
	print("This tool accepts a MegaVideo link, in the form of a complete URL")
	print("(such as http://www.megavideo.com/?[d/v]=XXXXXXXX), with the -u option,")
	print("or just the alphanumeric code (the 8-chars XXXXXXXX in the URL), with the")
	print("-c option, and checks whether the video is still available on MegaVideo.")
	print("If the video is either not existing or removed due to infringement, it")
	print("asks some regeneration databases and tries to provide alternative links.")
	print("If called with no options it prints just the links found (so this tool")
	print("can be used from another script). Use -d or -v for a more exhaustive")
	print("output.")
	print("You can also pass with the option -f a local file containg a list of")
	print("MegaVideo URLS to check. The file must contain a MegaVideo link on each")
	print("row. White rows are permitted, as comment lines (first char must be a #).")
	print("")
	print("Usage: mvregen.py [-u megavideourl | -c megavideocode | -f inputfile]")
	print("")
	print("Other options:")
	print("-d\tDebug info")
	print("-v\tVerbose (still less thank DEBUG)")
	print("-l N\tLimit the output to the first N found links (>=1!)")
	print("-o file\tPrints results in a text file")
	print("")
	print("If you pass an output file with the option -o, in that file at the end")
	print("of the process will be written the URLS (can be limited with the -l")
	print("option) and the comments from the original file in the right order.")
	print("")
	print("If you supply the megavideocode, the url will be formatted")
	print("as %sXXXXX."%baseMegavideoUrl)
	print("")
	print("If you do not use v (verbose) or d (debug), the tool only prints")
	print("out the found url(s) (or the supplied url if this is valid)")
	print("")

megaVideoUrls = []
megaVideoUrl = ""
inputFile = ""

outputFile = ""
outputFileData = []

try:
	opts, args = getopt.getopt(sys.argv[1:], "hu:c:vdl:f:o:")
except getopt.GetoptError:
	usage()
	sys.exit(0)

for o,a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-u":
		megaVideoUrls.append(a)
		log.info("Supplied %s url from command line"%a)
	elif o == "-c":
		megaVideoUrls.append("%s%s"%(baseMegavideoUrl, a))
	elif o == "-v":
		log.setLevel(logging.INFO)
		ch.setLevel(logging.INFO)
	elif o == "-d":
		log.setLevel(logging.DEBUG)
		ch.setLevel(logging.DEBUG)
	elif o == "-l":
		outputLimit = a
	elif o == "-f":
		inputFile = a
	elif o == "-o":
		outputFile = a

if (len(megaVideoUrls) == 0 and len(inputFile) == 0):
	usage()
	print("You need to provide an url, a MegaVideo code or an input file.\n")
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

# read input file and add elements to megaVideUrls array
# also add # comments, will just be printed on the output
if (len(inputFile) > 0):
	try:
		f = open(inputFile, 'r')
		for line in f:
			line = line.strip().rstrip('\n')	
			# skip empty lines
			if (len(line) == 0):
				continue
			megaVideoUrls.append(line)
		f.close()
	except:
		log.critical('Unable to open input file %s'%inputFile)
		sys.exit(1)
		
for megaVideoUrl in megaVideoUrls:
	
	# manage comment lines 
	if (megaVideoUrl.startswith('#')):
		commentLine = "######### %s"%megaVideoUrl.lstrip('#')
		log.info(commentLine)
		outputFileData.append(commentLine)
		continue

	# checks whether the url is available on MegaVideo
	availableOnMV = checkIfAvailableOnMV(megaVideoUrl)
	if (availableOnMV == -1):
		continue
	if (availableOnMV == 1):
		log.info("The original MegaVideo file has been removed due to infringiment")
	elif (availableOnMV == 2):
		log.info("The original MegaVideo file is not available")
	else:
		log.info("The url: %s is still available on MegaVideo."%megaVideoUrl)
		print("%s"%megaVideoUrl)
		outputFileData.append(megaVideoUrl)
		continue
	
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
		outputFileData.append(newLink)

# prints output file from output file data
if (len(outputFile) > 0):
	try:
		f = open(outputFile, 'w')
		for line in outputFileData:
			f.write("%s\n"%line)
		f.close()
		log.info("Written output data on file: %s"%outputFile)
	except:
		log.critical('Unable to open output file %s'%outputFile)
		sys.exit(1)
