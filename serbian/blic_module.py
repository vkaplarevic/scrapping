import urllib.request
from bs4 import BeautifulSoup
import news.comment
import time
# TODO: Change time to datetime.
# TODO: time module  sucks!!!

def __parse_date(raw):
    date_str = raw.split(", ")[1]
    append = ""
    if raw[-1] == "h":
        append = "h"
    return time.strptime(date_str, "%d. %m. %Y. %H:%M" + append)


def __read_parents(comment_box):
    classes = comment_box.get("class")
    if (len(classes) <= 3):
        return None

    return classes[-2].split("_")[1]


def parse_comments(link):
    site = urllib.request.urlopen(link + "/komentari#ostali");
    soup = BeautifulSoup(site.read(), "html.parser")
    site.close()

    main_content = soup.find("div", id="main_content")
    article_info = main_content.findAll("div")[0].find("span")
    date_str = article_info.text
    article_date = __parse_date(date_str)

    comments = {}
    comment_boxes = soup.findAll("div", class_="comment_box")
    for comment_box in comment_boxes:
        ic = __parse_one_comment(comment_box)
        if not ic:
            continue
        comments[ic.unique_id] = ic

    parent_graph = {c: [] for c in comments}
    for cid in comments:
        comm = comments[cid]
        if not comm.parent_id:
            continue
        parent_graph[comm.parent_id].append(comm.unique_id)

    return news.comment.CommentStats(comments, parent_graph, article_date)


def __parse_one_comment(comment_box):
    # Parse one comment for from the HTML comment box element.
    # ...
    dev_text = comment_box.find("div", class_="comm_text")
    if dev_text is None:
        return None

    date_element = comment_box.find("span", class_="u_info")
    p_comment_date = __parse_date(date_element.text) 

    p_text = dev_text.get_text()
    name_holder = comment_box.find("div", class_="comm_u_name")
    name_holder_span = name_holder.find("span")
    p_author = name_holder_span.get_text()

    plus_div = comment_box.find("div", class_="voteplus")
    plus_span = plus_div.find("span")
    p_pluses_count = int(plus_span.get_text()) if plus_span is not None else 0

    minus_div = comment_box.find("div", class_="voteminus")
    minus_span = minus_div.find("span")
    p_minuses_count = int(minus_span.get_text()) if minus_span is not None else 0

    p_unique_id = comment_box.get("db_id")
    p_parent_id = __read_parents(comment_box)

    ic = news.comment.Comment(text=p_text, author=p_author, pluses=p_pluses_count, minuses=p_minuses_count, unique_id=p_unique_id, time = p_comment_date)
    if p_parent_id is not None:
        ic.parent_id = p_parent_id

    return ic





