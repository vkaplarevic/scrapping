#!/usr/bin/env python

import sys
import blic_module


def main():
    if len(sys.argv) == 1:
        return

    link = sys.argv[1]
    print("Parsing comments: " + link)

    stats = blic_module.parse_comments(link)
    print(str(stats))

main()


