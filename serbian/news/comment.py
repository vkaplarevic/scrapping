import time
import datetime
"""
Simple class encapsulating comment on various internet sites.
"""

def _num_format(num):
    return "0" + str(num) if num < 10 else str(num)

def _round_time(st_raw):
    date_str = str(st_raw.tm_year) + "-" + _num_format(st_raw.tm_mon) + "-" + _num_format(st_raw.tm_mday) + " " + _num_format(st_raw.tm_hour) + ":00" 
    return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M") 


class Comment(object):
    """
    Comment class. Encapulates following data regarding the comment:
        text, author, number of approvals, number of minuses, and unique_id

    """
    def __init__(self, text, author, pluses=0, minuses=0, unique_id=None, time=None):
        self.text = text
        self.author = author
        self.pluses = pluses
        self.minuses = minuses
        # Each comment has to have a unique id. If not available in the page
        # one needs to be created while parsing.
        self.unique_id = unique_id
        self.parent_id = None
        self.time = time


    def __str__(self):
        res = "author: " + self.author + "\n"
        res += "text: " + self.text + "\n"
        res += "pluses: " + str(self.pluses) + "\n"
        res += "minuses: " + str(self.minuses) + "\n"
        res += "unique_id: " + str(self.unique_id) + "\n"
        res += "time: " + self.formatted_time() + "\n"
        return res


    def get_replies_count(self, comment_ids, comment_graph):
        count = 0
        for cid in comment_graph[self.unique_id]:
            count += 1 + comment_ids[cid].get_replies_count(comment_ids, comment_graph)
        return count


    def formatted_time(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S", self.time) + "\n"



class CommentStats:
    """
    Basic stats about the comments on one page.
    """
    def __init__(self, comment_ids, comment_graph, article_date):
        """
        comment_ids: dictionary of ids mapping to comment object,
        comment_graph: graph mapping the comment id to its children
        """
        self.comment_ids = comment_ids
        self.graph = comment_graph
        self.article_date = article_date
        self._create_stats()



    def _create_stats(self):
        """
        Create statistics for the coments.
        """
        self.total_count = len(self.comment_ids)

        cid = max(self.graph.keys(), key=lambda x: len(self.graph[x]))
        self.max_replies_comment = self.comment_ids[cid]

        cid = max(self.comment_ids.keys(), key=lambda x: self.comment_ids[x].pluses)
        self.max_pluses_comment = self.comment_ids[cid]

        cid = max(self.comment_ids.keys(), key=lambda x: self.comment_ids[x].minuses)
        self.max_minuses_comment = self.comment_ids[cid]

        # Author by number of comments:
        self.author_comment = {self.comment_ids[c].author: 0 for c in self.comment_ids}
        for cid in self.comment_ids:
            self.author_comment[self.comment_ids[cid].author] += 1

        # Calculate how many replies each author received:
        self.author_replies = {
            self.comment_ids[c].author: 
            self.comment_ids[c].get_replies_count(self.comment_ids, self.graph) for c in self.comment_ids
        }

        self.comments_chronologically = sorted(
                [x for x in  self.comment_ids.keys()],
                key=lambda c: self.comment_ids[c].time
        )

    def __str__(self):
        res = "Statistics:\n"
        res += "* Article date: " + time.strftime("%a, %d %b %Y %H:%M:%S", self.article_date) + "\n"
        res += "* Total number of comments: " + str(self.total_count) + "\n"
        res += "* Comment with most replies:\n" + str(self.max_replies_comment) + "\n"
        res += "* Comment with most pluses:\n" + str(self.max_pluses_comment) + "\n"
        res += "* Comment with most minuses:\n" + str(self.max_minuses_comment) + "\n"
        return res

    def comments_per_hour(self):
        st = _round_time(self.comment_ids[self.comments_chronologically[0]].time)
        et = _round_time(self.comment_ids[self.comments_chronologically[-1]].time)
        time = _round_time(self.comment_ids[self.comments_chronologically[0]].time)
        ranges = {}
        while time <= et:
            ranges[time] = []
            time = time + datetime.timedelta(hours=1)

        for cid in self.comment_ids:
            comment = self.comment_ids[cid].time
            rounded = _round_time(self.comment_ids[cid].time)
            ranges[rounded].append(cid)

        return {x: len(ranges[x]) for x in ranges}

