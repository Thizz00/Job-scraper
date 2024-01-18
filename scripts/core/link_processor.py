import requests
from bs4 import BeautifulSoup
import concurrent.futures
import logging

SCRAP_LINK1 = 'https://rocketjobs.pl'
SCRAP_LINK2 = 'https://nofluffjobs.com/'
SCRAP_LINK3 = 'https://justjoin.it'


class LinkProcessor:
    def __init__(self, urls):
        self.urls = urls
        self.scraped_links = set()

    def get_html_document(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching URL {url}: {str(e)}")
            return None

    def process_generic_url(self, soup, url, div_class, link_prefix):
        divs = soup.find_all('div', class_=div_class)
        for div in divs:
            anchor_tags = div.find_all('a', href=True)
            for tag in anchor_tags:
                href = tag['href']
                self.scraped_links.add(link_prefix + href)

    def process_first_link_url(self, soup, url):
        self.process_generic_url(soup, url, [
                                 'css-1tksz28', 'css-6xbxgh', 'css-1tksz28', 'MuiBox-root css-q72hon', 'css-ih8c0d'], SCRAP_LINK1)

    def process_second_link_url(self, soup, url):
        self.process_generic_url(
            soup, url, ['list-container ng-star-inserted'], SCRAP_LINK2)

    def process_third_link_url(self, soup, url):
        self.process_generic_url(
            soup, url, ['css-2crog7', 'css-10fd0p8'], SCRAP_LINK3)

    def process_url(self, url):
        try:
            html_document = self.get_html_document(url)
            if html_document is not None:
                soup = BeautifulSoup(html_document, 'html.parser')
                if STR_LINK1 in url:
                    self.process_first_link_url(soup, url)
                elif STR_LINK2 in url:
                    self.process_second_link_url(soup, url)
                elif STR_LINK3 in url:
                    self.process_third_link_url(soup, url)
                logging.info(f"Successfully processed URL: {url}")
        except Exception as e:
            logging.error(f"Error processing URL {url}: {str(e)}")

    def process_urls(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(self.process_url, url)
                       for url in self.urls]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Thread error: {str(e)}")