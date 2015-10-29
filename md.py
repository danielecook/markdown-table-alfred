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

__version__ = '0.1'


def main(wf):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`

    # Get args from Workflow as normalized Unicode
    args = wf.args

    cb = pyperclip.paste().strip()

    try:
        dialect = csv.Sniffer().sniff(StringIO(cb).read(1024))
        cb = list(csv.reader(StringIO(unicode(cb), newline=None), dialect))
    except:
        cb = [x.split("\t")  for x in re.sub(" +","\t", cb).split("\n")]

    try:
        # Header
        cb_grid_header = tabulate(cb,  headers="firstrow", tablefmt="pipe")
        cb_grid_header_prev = "L1: " + cb_grid_header.split("\n")[0] + ";L2: " + cb_grid_header.split("\n")[2]
        wf.add_item("Header", cb_grid_header_prev, arg=cb_grid_header, valid=True)
      
        # No header
        cb_grid = tabulate(cb, tablefmt="pipe")
        cb_grid_prev = cb_grid.split("\n")[1]

        wf.add_item("No Header", cb_grid_prev, arg=cb_grid, valid=True)
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

