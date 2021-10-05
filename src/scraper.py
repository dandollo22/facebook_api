from datetime import datetime
import uuid as _uuid
import os
import time as _time
import yaml as _yaml
from selenium import webdriver
from sys import platform
from bs4 import BeautifulSoup
import logging as _logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.facebook.com"


class FacebookScraper:

    def __init__(self, headless="phantomjs", browser=None, webdriver_path=None):
        """
        Args:
            headless (str): Headless tool name.
            browser (str): Browser to run selenium.
            webdriver_path (str): Specific web driver path other than default.
        """

        with open(os.path.join(BASE_DIR, "config", "settings.yaml")) as file:
            self.settings = _yaml.load(file)

        self.platform = "linux"

        if platform == "win32":
            self.platform = "windows"
        elif platform == "darwin":
            self.platform = "mac"

        if browser:
            self.webdriver_path = os.path.join(BASE_DIR, "webdrivers", self.platform,
                                               self.settings["webdrivers"][browser][self.platform])
        elif webdriver_path:
            self.webdriver_path = webdriver_path
        else:
            self.webdriver_path = os.path.join(BASE_DIR, "webdrivers", self.platform,
                                               self.settings["webdrivers"][headless][self.platform])

        if browser == "chrome":
            self.driver = webdriver.Chrome(self.webdriver_path)
        elif browser == "firefox":
            self.driver = webdriver.Firefox(self.webdriver_path)
        else:
            self.driver = webdriver.PhantomJS(self.webdriver_path)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.driver.quit()

    # utils functions
    @staticmethod
    def make_url2id(url):
        """ turns url into hashcode in order to use as a unique id"""
        guid = _uuid.uuid5(_uuid.NAMESPACE_URL, url)
        return str(guid.int)

    def scroll(self, scroll_pause_time=0.5):
        """Scrolls through page with selenium"""
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            _time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            _time.sleep(1)

    # element accessors
    def get_link(self, bs_element: BeautifulSoup):
        return bs_element.find('a', {'class': '_5pcq'})['href']

    def get_date(self, bs_elem: BeautifulSoup):
        return bs_elem.find('abbr')['data-tooltip-content']

    def get_likes(self, bs_elem: BeautifulSoup):
        return bs_elem.find('span', {'class': '_3dlg'})

    def get_comments(self, bs_elem: BeautifulSoup):
        return bs_elem.find('span', {'class': '_4vn2'})

    def get_shares(self, bs_elem: BeautifulSoup):
        return bs_elem.find('span', {'class': '_355t _4vn2'})

    def get_posts(self, page_ext: str):
        """scrapes facebook pages data"""
        try:
            url = "{}/{}/".format(BASE_URL, page_ext)
            self.driver.get(url)
            self.scroll()
            # ignores the sign-in panel
            try:
                self.driver.find_element_by_class_name('_62up').click()
            except:
                pass
            _time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            # get publication elements
            publication_elem = soup.find_all('div', {'class': '_5pcr userContentWrapper'})

            data_collector = dict()
            data_collector[page_ext] = list()

            for elem in publication_elem:
                date = self.get_date(elem)
                post_url = BASE_URL + self.get_link(elem)
                likes = self.get_likes(elem)
                comments = self.get_comments(elem)
                shares = self.get_shares(elem)
                post_id = FacebookScraper().make_url2id(post_url),

                data = {
                    "id": post_id[0],
                    "page": page_ext,
                    "post_url": post_url,
                    "shared_at": date,
                    "likes": likes.text if likes is not None else '0',
                    "comments": comments.text.replace('commentaires', '') if comments is not None else '0',
                    "shares": shares.text.replace('partages', '') if shares is not None else '0',
                    "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
                data_collector[page_ext].append(data)
                _logging.info(f"Collected {len(data_collector[page_ext])} new publication")
        finally:
            self.driver.close()
        return data_collector
