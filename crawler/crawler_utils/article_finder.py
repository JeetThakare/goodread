import requests
from bs4 import BeautifulSoup
import unicodedata
from crawler.models import Article


def get_post(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    divs = soup.find_all(
        'div', {'class': 'section-inner sectionLayout--insetColumn'})
    content = ' '.join([div.get_text(strip=True) for div in divs])
    content = unicodedata.normalize("NFKD", content)
    return content


def save_post_from(link):
    if ("/p/" in link) or ("/s/" in link):
        print("finding post on: ", link)
        content = get_post(link)
        if content:
            new_article = Article(article=content, url=link)
            try:
                new_article.save()
            except Exception as e:
                print(e)
                exit(1)
