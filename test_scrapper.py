from unittest import TestCase, main
import src.scraper as _scraper


class TestHelloWorld(TestCase):

    def test_publication_elements(self):
        scraper = _scraper.FacebookScraper(browser='chrome')
        data = scraper.get_posts('8fact')
        self.assertGreater(len(data), 0)


if __name__ == '__main__':
    main()
