from urllib.request import urlopen
from urllib.request import Request as req
from crawler.crawler_utils.link_finder import LinkFinder
from crawler.models import Link
from crawler.crawler_utils.utils import get_domain_name
import requests

# Adapted version of https://github.com/buckyroberts/Spider


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        q = Link.objects.filter(visited=False).all()
        Spider.queue = set([l.url for l in q])
        c = Link.objects.filter(visited=True).all()
        Spider.crawled = set([l.url for l in c])

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) +
                  ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_db()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            my_url = page_url
            headers = {'User-Agent': user_agent}
            complete_request = req(my_url, None, headers)
            response = urlopen(complete_request)
            # response = requests.get(page_url)

            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, response.url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_db():

        for a in Spider.queue.copy():
            l = Link(url=a, visited=False)
            try:
                l.save()
            except:
                pass
        for a in Spider.crawled.copy():
            l = Link(url=a, visited=True)
            try:
                l.save()
            except:
                pass
