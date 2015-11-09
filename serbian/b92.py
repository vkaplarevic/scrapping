#!/usr/bin/env python

import sys
import b92_module

import plotly.plotly as py
import plotly.graph_objs as go
import time


def main():
    if len(sys.argv) == 1:
        return

    link = sys.argv[1] 
    stats = b92_module.parse_comments(link) 


main()


