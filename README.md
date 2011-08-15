# Megavideo Link Cleaner

This tool accepts a MegaVideo link, in the form of a complete URL
(such as http://www.megavideo.com/?[d/v]=XXXXXXXX), with the -u option,
or just the alphanumeric code (the 8-chars XXXXXXXX in the URL), with the
-c option, and checks whether the video is still available on MegaVideo.
If the video is either not existing or removed due to infringement, it
asks some regeneration databases and tries to provide alternative links.
If called with no options it prints just the links found (so this tool
can be used from another script). Use -d or -v for a more exhaustive
output.
You can also pass with the option -f a local file containg a list of
MegaVideo URLS to check. The file must contain a MegaVideo link on each
row. White rows are permitted, as comment lines (first char must be a #).

Usage: mvregen.py [-u megavideourl | -c megavideocode | -f inputfile]

Other options:

* -h	This help
* -d	    Debug info
* -v	    Verbose (still less thank DEBUG)
* -l N	    Limit the output to the first N found links (>=1!)
* -o file	Prints results in a text file
* -t	Prints the output file in HTML format

If you pass an output file with the option -o, in that file at the end
of the process will be written the URLS (can be limited with the -l
option) and the comments from the original file in the right order. 

If you supply the megavideocode, the url will be formatted
as http://www.megavideo.com/?v=XXXXX.

# Megavideo URL Parser

This tool accepts a valid URL and prints a list of all the MegaVideo
links found in the page (see SCAN MODE later).
If called with no options it prints just the links found (so this tool
can be used from another script). Use -d or -v for a more exhaustive
output.

Usage: mvparse.py -u URL

Other options:

* -h	This help
* -d	Debug info
* -v	Verbose (still less thank DEBUG)
* -r	Raw scan mode

SCAN MODE

* 0: Default mode. Searches for links in the form
   <a href="http://www.megavideo.com/?[v/d]=XXXXXXX">Description</a>
   and prints an output formatted like:
     
   # Description
   
   http://www.megavideo.com/?[v/d]=XXXXXXX
   
   This mode is useful to create input files for the mvregen tool.

* 1: Raw mode. Searches for every occurrence of the regexp
   http://www.megavideo.com/?[v/d]=XXXXXXX
