#!/usr/bin/env python

import sys
import b92_module


def main():
    if len(sys.argv) == 1:
        return

    link = sys.argv[1] 
    comments = b92_module.parse_comments(link) 




main()


