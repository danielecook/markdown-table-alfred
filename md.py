#!/usr/bin/python
# encoding: utf-8

import sys
import re

from workflow import Workflow, ICON_WEB, web
import pyperclip
from tabulate import tabulate
import csv
from io import StringIO
import re
import sys

__version__ = '0.2'


def main(wf):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`

    # Get args from Workflow as normalized Unicode
    delim = wf.args
    cb = pyperclip.paste().strip()

    custom = ""
    if len(delim[0]) == 0:
        try:
            dialect = csv.Sniffer().sniff(StringIO(cb).read(1024))
            cb = list(csv.reader(StringIO(unicode(cb), newline=None), dialect))
        except:
            cb = [x.decode('utf-8').split(delim)  for x in re.sub(" +","\t", cb).split("\n")]
    else:
        # Custom delimiter
        custom = " - Custom ==> " + str(delim[0])
        cb = [re.split(delim[0], x) for x in cb.decode("utf-8").split("\n")]
        log.debug(cb)

    try:
        # Header
        cb_grid_header = tabulate(cb,  headers="firstrow", tablefmt="pipe")
        cb_grid_header_prev = "L1: " + cb_grid_header.split("\n")[0] + ";L2: " + cb_grid_header.split("\n")[2]
        wf.add_item("Header" + custom, cb_grid_header_prev, arg=cb_grid_header, valid=True)
      
        # No header
        cb_grid = tabulate(cb, tablefmt="pipe")
        cb_grid_prev = cb_grid.split("\n")[1]

        wf.add_item("No Header" + custom, cb_grid_prev, arg=cb_grid, valid=True)
    except:
        wf.add_item("Error", "Unable to parse table", icon = "error.png")


    
    # Send output to Alfred
    #log.debug(wf.send_feedback())
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'danielecook/md',
        'version': __version__,
        'frequency': 7
        })
    if wf.update_available:
        # Download new version and tell Alfred to install it
        wf.start_update()
    log = wf.logger
    sys.exit(wf.run(main))

