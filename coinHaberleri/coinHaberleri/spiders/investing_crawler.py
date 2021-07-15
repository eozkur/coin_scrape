import scrapy
from bs4 import BeautifulSoup
import json


##
# In order to avoid writing the same articles to database over and over again, I will hold the last batch and compare
# freshly scraped news against it.
# You have to be in the upper coinHaberleri directory to run this spider
# Run scrapy crawl investing_crawler -o news.json in order to get news from investing.com and write them into news.json


class ExampleSpider(scrapy.Spider):
    name = "investing_crawler"  # Name this for related website ie coindesk_crawler

    allowed_domains = ['coindesk.com',  # Use only one website
                       'investing.com',
                       'coinmarketcap.com',
                       'yahoo.com',
                       'cryptonews.com']

    start_urls = ['https://www.investing.com/news/cryptocurrency-news']  # Whatever pages I want to crawl
    url = ""  # These are abominations :/
    urltophoto = ""  # but they are necessary in order to create a single object for each article
    summary = ""  # Passing these as arguements to parse_news didn't work

    def parse(self, response):
        photoUrls = response.css('div.largeTitle article img::attr(data-src)').getall()  # get all photo urls
        urls = response.css('div.largeTitle article a.img::attr(href)').getall()  # get all article urls
        summary = response.css('div.largeTitle article p').getall()  # get all summaries
        title = response.css('div.largeTitle article a.title::text').getall()  # get all summaries
        ago = response.css('div.largeTitle article span.date').getall()  # get all summaries

        print(ago)                          # used for validation of above variables

        for i in range(len(summary)):


            rettext = ""  # As in text to be returned,
            for html in summary[i]:  # <p>'s include <span>'s, beautiful soup gets rid of them
                rettext += html
            soup = BeautifulSoup(rettext, features="lxml")

            self.urltophoto = photoUrls[i]  # get the current photo url
            self.url = urls[i]  # get the current url

            if self.url[0] != 'h':  # urls that start with https are external links I don't like them.
                self.summary = soup.get_text()

                yield scrapy.Request(response.urljoin(self.url), self.parse_news)

    def parse_news(self, response):
        ret = response.css('div.articlePage p').getall()
        date = response.css('div.contentSectionDetails span::text').get()
        date = date.split('(')[1].split(')')[0]
        #print(date)

        rettext = ""

        for html in ret[:-1]:
            rettext += html
        soup = BeautifulSoup(rettext, features="lxml")
        article = soup.get_text()

        news = {
            "article": article,
            'summary': self.summary,
            "url": self.url,
            "photo": self.urltophoto
        }

        with open('data.json', 'w') as f:
            json.dump(news, f)

        # yield {
        #     "article": article,
        #     'summary': self.summary,
        #     "url": self.url,
        #     "photo": self.urltophoto
        # }
