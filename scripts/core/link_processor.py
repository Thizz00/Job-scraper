import os
import sys
import asyncio
import aiohttp
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.logs_configure.logger_config import configure_logger

logger = configure_logger(__name__)

SCRAP_LINK1 = 'https://rocketjobs.pl'
SCRAP_LINK2 = 'https://nofluffjobs.com/'
SCRAP_LINK3 = 'https://justjoin.it'


class LinkProcessor:
    def __init__(self, urls):
        self.urls = urls
        self.scraped_links = set()

    async def get_html_document(self, session, url):
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            logger.error(f"Error occurred while fetching URL: {url}, Error: {str(e)}")
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

    async def process_url(self, session, url):
        html_document = await self.get_html_document(session, url)
        if html_document is not None:
            soup = BeautifulSoup(html_document, 'html.parser')
            if SCRAP_LINK1 in url:
                self.process_first_link_url(soup, url)
            elif SCRAP_LINK2 in url:
                self.process_second_link_url(soup, url)
            elif SCRAP_LINK3 in url:
                self.process_third_link_url(soup, url)
            logger.info(f"Successfully processed URL: {url}")

    async def process_urls(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.process_url(session, url) for url in self.urls]
            await asyncio.gather(*tasks)
