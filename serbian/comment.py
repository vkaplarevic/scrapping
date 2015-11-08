"""
Simple class encapsulating comment on various internet sites.
"""

class Comment(object):
    """
    Comment class. Encapulates following data regarding the comment:
        text, author, number of approvals, number of minuses, and unique_id

    """
    def __init__(self, text, author, pluses=0, minuses=0, unique_id=None):
        self.text = text
        self.author = author
        self.pluses = pluses
        self.minuses = minuses
        # Each comment has to have a unique id. If not available in the page
        # one needs to be created while parsing.
        self.unique_id = unique_id
        self.parent_id = None


    def __str__(self):
        res = "author: " + self.author + "\n"
        res += "text: " + self.text + "\n"
        res += "pluses: " + str(self.pluses) + "\n"
        res += "minuses: " + str(self.minuses) + "\n"
        res += "unique_id: " + str(self.unique_id) + "\n"
        return res


    def get_replies_count(self, comment_ids, comment_graph):
        count = 0
        for cid in comment_graph[self.unique_id]:
            count += 1 + comment_ids[cid].get_replies_count(comment_ids, comment_graph)
        return count


class CommentStats:
    """
    Basic stats about the comments on one page.
    """
    def __init__(self, comment_ids, comment_graph):
        """
        comment_ids: dictionary of ids mapping to comment object,
        comment_graph: graph mapping the comment id to its children
        """
        self.comment_ids = comment_ids
        self.graph = comment_graph
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
        # calculate how many replies each author received:
        self.author_replies = {
                self.comment_ids[c].author: 
                self.comment_ids[c].get_replies_count(self.comment_ids, self.graph) for c in self.comment_ids
                }

    def __str__(self):
        res = "Statistics:\n"
        res += "* Total number of comments: " + str(self.total_count) + "\n"
        res += "* Comment with most replies:\n" + str(self.max_replies_comment) + "\n"
        res += "* Comment with most pluses:\n" + str(self.max_pluses_comment) + "\n"
        res += "* Comment with most minuses:\n" + str(self.max_minuses_comment) + "\n"

        return res


