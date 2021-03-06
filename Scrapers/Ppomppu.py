# coding: utf-8

import csv
import requests
from urllib.parse import urljoin, urlparse
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

        url = 'https://www.fmkorea.com/index.php'\
              + f'?mid=home&act=IS&search_target=title&is_keyword={self.query}&where=document&page={page}'
        soup = self.get_soup(url)

        links = []
        for li in soup.find_all('li', {'class': ''}):
            dl = li.find('dl')
            if dl:
                a = dl.find('a')
                full_url = urljoin(url, a.get('href'))
                links.append(full_url)

        return links

    def get_content_from_page(self, url: str) -> dict:
        """
        Get title, contents from Article URL. It returns title + content by str.
        """

        soup = self.get_soup(url)
        title = soup.find('span', {'class': 'np_18px_span'}).text
        content = soup.find('article', {'class': ''}).text

        return {'title': title, 'content': content}

    def get_emotions(self):
        csv_file = open('Ppomppu.csv', 'w', newline='', encoding='UTF-8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(('#', 'title', 'content', 'posneg'))

        index = 1
        for i in range(10):
            articles = self.get_links_from_page(i+1)
            for article in articles:
                # article is the url of the article
                contents = self.get_content_from_page(article)
                title = contents.get('title')
                content = contents.get('content')
                emotion = Emotion.get_emotion(title + content)

                csv_writer.writerow((index, title, content, emotion))
                index += 1

                print(f'[ INFO ] {title}, {emotion}')

        csv_file.close()


if __name__ == '__main__':
    es = EmotionScraper('대마')
    es.get_emotions()

