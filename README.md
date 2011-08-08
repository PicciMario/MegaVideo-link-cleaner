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

Usage: mvregen.py [-u megavideourl | -c megavideocode]

Other options:

* -d	Debug info
* -v	Verbose (still less thank DEBUG)
* -l N	Limit the output to the first N found links (>=1!)

If you supply the megavideocode, the url will be formatted
as http://www.megavideo.com/?v=XXXXX.

# Megavideo URL Parser

This tool accepts a valid URL and prints a list of all the MegaVideo
links (in the form http://www.megavideo.com/?[d/v]=XXXXXXXX) found in
the page. If called with no options it prints just the links found
(so this tool can be used from another script). Use -d or -v for a more
exhaustive output.

Usage: mvparse.py -u URL

Other options:

* -d	Debug info
* -v	Verbose (still less thank DEBUG)
