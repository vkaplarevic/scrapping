#!/usr/bin/env python

import sys
import blic_module

import plotly.plotly as py
import plotly.graph_objs as go


def main():
    if len(sys.argv) == 1:
        return

    link = sys.argv[1]
    print("Parsing comments: " + link)

    stats = blic_module.parse_comments(link) 
    author_replies = stats.author_replies
    author_comment = stats.author_comment
    values = [x for x in author_replies.keys() if author_replies[x] > 0]
    
    comments_per_hour = stats.comments_per_hour()
    times = [x for x in comments_per_hour]
    data = [
        go.Bar(
            x=times,
            y=[comments_per_hour[x] for x in times]
        )
    ]
    plot_url = py.plot(data, filename='comments-per-time')
    print("You can find you graph here: " + plot_url)

    # data = [
    #     go.Bar(
    #         x=values,
    #         y=[author_replies[x] for x in values]
    #     ),
    #     go.Bar(
    #         x=values,
    #         y=[author_comment[x] for x in values]
    #     )]
    # plot_url = py.plot(data, filename='comments-replies')
    # print(plot_url)
    #

main()
