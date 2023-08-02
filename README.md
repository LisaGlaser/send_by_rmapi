# send_by_rmapi
This is a calibre plugin, to send epub or pdf files saved with Calibre to the reMarkable tablet.

To send file(s) mark them in the Calibre GUI and just add press [Ctrl-Shift-S]. Or just add a button to your Calibre GUI.

It uses the rmapi commandline interface https://github.com/juruen/rmapi which you will need to set up.

Currently the plugin assumes that rmapi does not need a password and that the folder on the tablet should already exist.

To install the plugin in calibre use the command line

`calibre-debug -s; calibre-customize -b /path/to/send_by_rmapi; calibre`
