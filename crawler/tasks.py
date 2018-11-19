from crawler.models import Link
import threading
from queue import Queue
from crawler.crawler_utils.spider import Spider
from crawler.crawler_utils.utils import get_domain_name
from crawler.crawler_utils.article_finder import save_post_from

PROJECT_NAME = 'medium'
HOMEPAGE = 'https://medium.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
NUMBER_OF_THREADS = 20
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Create worker threads (will die when main exits)


def create_workers(linkonly=True):
    for _ in range(NUMBER_OF_THREADS):
        if linkonly:
            t = threading.Thread(target=work)
        else:
            t = threading.Thread(target=fetch)
        t.daemon = True
        t.start()


def fetch():
    while True:
        url = queue.get()
        save_post_from(url)
        queue.task_done()

# Do the next job in the queue


def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs(linkonly=True):
    if linkonly:
        links = Link.objects.all().filter(visited=False)
    else:
        links = Link.objects.all().filter(article_fetched=False)
    for link in links:
        queue.put(link.url)
    queue.join()
    crawl(linkonly)


# Check if there are items in the queue, if so crawl them
def crawl(linkonly=True):
    if linkonly:
        queued_links = Link.objects.all().filter(visited=False)
    else:
        queued_links = Link.objects.all().filter(article_fetched=False)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs(linkonly)
    else:
        print("Done!")
        exit()


def fetch_links():
    create_workers()
    crawl()


def fetch_articles():
    create_workers(linkonly=False)
    crawl(linkonly=False)
