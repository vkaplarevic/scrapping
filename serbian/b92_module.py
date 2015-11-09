import urllib.request
from bs4 import BeautifulSoup
import news.comment
import time
import urllib



SERBIAN_MONTHS = {
    'januar':   '01',
    'februar':  '02',
    'mart':     '03',
    'april':    '04',
    'maj':      '05',
    'jun':      '06',
    'jul':      '07',
    'avgust':   '08',
    'septembar':'09',
    'oktobar':  '10',
    'novembar': '11',
    'decembar': '12'
}



def __parse_date(raw):
    which = None
    for name in SERBIAN_MONTHS:
        if name in raw:
            which = name
            break

    time_str = raw.replace(which, SERBIAN_MONTHS[which] + ".")
    return time.strptime(time_str, "%d. %m. %Y %H:%M")

def __get_comments_link(link):
    url_args = urllib.parse.urlparse(link)
    query = urllib.parse.parse_qs(url_args.query)
    nav_id = query['nav_id'][0]
    url = "http://www.b92.net/biz/komentari.php?nav_id=" + nav_id 
    return url


def __extract_number(raw):
    return int("".join([x for x in list(raw) if x.isdigit()]))
   
def __parse_one_comment(el):
    p_unique_id = el.get('id')
    p_text = el.text
    p_author = el.findAll("span", class_="comment-author")[0].text
    p_time = __parse_date(el.findAll("span", class_="comment-date")[0].text) 
    
    pluses_raw = el.findAll("a", class_="rate-up")[0].findAll("span")[0].text
    p_pluses = __extract_number(pluses_raw)
    
    minuses_raw = el.findAll("a", class_="rate-up")[0].findAll("span")[0].text
    p_minuses = __extract_number(minuses_raw)

    ic = news.comment.Comment(text=p_text, author=p_author, pluses=p_pluses, minuses=p_minuses, unique_id=p_unique_id, time = p_time)

    return ic

def parse_comments(link):
    url = __get_comments_link(link) 
    site = urllib.request.urlopen(url);
    soup = BeautifulSoup(site.read(), "html.parser")
    site.close()
  
    comments_box_wrapper = soup.findAll("div", id="tab-comments-h-tab") 
    comments_ol = comments_box_wrapper[0].findAll("ol")
    comments = {}
    for li in comments_ol[0].findAll("li"):
        ic = __parse_one_comment(li)
        if not ic:
            continue
        comments[ic.unique_id] = ic


    parent_graph = {c: [] for c in comments}
    for cid in comments:
        comm = comments[cid]
        if not comm.parent_id:
            continue
        parent_graph[comm.parent_id].append(comm.unique_id)

    return news.comment.CommentStats(comments, parent_graph)



