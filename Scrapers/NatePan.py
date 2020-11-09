# coding: utf-8

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from lib import Emotion


class EmotionScraper:
    def __init__(self, query: str):
        self.query = query
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }

    def get_soup(self, url: str) -> BeautifulSoup:
        """
        Get BeautifulSoup from url
        """

        resp = self.session.get(url)
        return BeautifulSoup(resp.text, 'lxml')

    def get_links_from_page(self, page: int) -> list:
        """
        Get <a href="*"> from Listing Page
        """

        url = f'https://pann.nate.com/search/talk?q={self.query}&page={page}'
        soup = self.get_soup(url)

        links = []
        for subject in soup.find_all('a', {'class': 'subject'}):
            full_url = urljoin(url, subject.get('href'))
            links.append(full_url)

        return links

    def get_content_from_page(self, url) -> dict:
        """
        Get title, contents from Article URL. It returns title + content by str.
        """

        soup = self.get_soup(url)
        title = soup.find_all('h4')[0].text
        content = soup.find_all('div', {'id': 'contentArea'})[0].text

        return {'title': title, 'content': content}

    def get_emotions(self):
        for i in range(10):
            articles = self.get_links_from_page(i+1)
            for article in articles:
                # article is the url of the article
                contents = self.get_content_from_page(article)
                title = contents.get('title')
                content = contents.get('content')
                emotion = Emotion.get_emotion(title + content)
                print(f'[ INFO ] {title}, {emotion}')


if __name__ == '__main__':
    es = EmotionScraper('대마')
    es.get_emotions()
