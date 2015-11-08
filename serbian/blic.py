#!/usr/bin/env python

import sys
import blic_module

import plotly.plotly as py
import plotly.graph_objs as go


def create_barchart_per_hour(link):
    stats = blic_module.parse_comments(link) 
    
    comments_per_hour = stats.comments_per_hour
    highest_rated_comment_per_hour = stats.highest_rated_comment_per_hour
    times = [x for x in comments_per_hour]

    data = [
        go.Bar(
            name="Comments breakdown for: " + link,
            x=times,
            y=[len(comments_per_hour[x]) for x in times],
            text=[str(highest_rated_comment_per_hour[x]) for x in times],
        ),
    ]

    plot_url = py.plot(data, filename='comments-per-time-' + link.replace("/", "_") )
    print("You can find you graph here: " + plot_url)


def main():
    if len(sys.argv) == 1:
        return

    link = sys.argv[1]
    create_barchart_per_hour(link)


main()



