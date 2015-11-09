#!/usr/bin/env python

import sys
import blic_module

import plotly.plotly as py
import plotly.graph_objs as go
import time

def create_barchart_per_hour(stats):
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

    plot_url = py.plot(data, filename='cpl_' + link)
    print("You can find you graph here: " + plot_url)


def create_barchart_all_comments(stats):
    comment_ids = stats.comment_ids
    comments_chronologically = stats.comments_chronologically

    times  = [
        time.strftime("%d %b %Y %H:%M:%S", comment_ids[x].time) for x in comments_chronologically
    ]
    pluses = [
        comment_ids[x].minuses for x in comments_chronologically
    ]
    textes = [ 
        comment_ids[x].html() for x in comments_chronologically
    ]
    data = [
        go.Bar(
            name="all comments",
            x=times,
            y=pluses,
            text=textes
        ),
    ]

    plot_url = py.plot(data, filename='all_commentes')
    print("You can find you graph here: " + plot_url)


def main():
    if len(sys.argv) == 1:
        return

    link = sys.argv[1] 
    stats = blic_module.parse_comments(link) 
    
    # create_barchart_per_hour(link)
    create_barchart_all_comments(stats)

main()



