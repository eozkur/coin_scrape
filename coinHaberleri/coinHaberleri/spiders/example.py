import scrapy
from  bs4 import BeautifulSoup

class ExampleSpider(scrapy.Spider):
    
    name = "investing_crawler"  # Name this for related website ie coindesk_crawler
    
    allowed_domains = ['coindesk.com',      # Use only one website
                       'investing.com',
                       'coinmarketcap.com',
                       'yahoo.com',
                       'cryptonews.com']

    start_urls = ['https://www.investing.com/news/cryptocurrency-news'] # Whatever pages I want to crawl 
    url = ""            #   These are abominations :/
    urltophoto = ""     #   but they are necessary in order to create a single object for each article
    summary = ""           #   Passing these as arguements to parse_news didn't work

    def parse(self, response):
        photoUrls = response.css('div.largeTitle article img::attr(data-src)').getall() # get all photo urls
        urls = response.css('div.largeTitle article a.img::attr(href)').getall()        # get all article urls
        summary = response.css('div.largeTitle article p').getall()                     # get all summaries

        #print(summary, len(photoUrls), len(urls),len(summary))                          # used for validation of above variables

        for i in range(len(summary)):

            rettext = ""                    # As in text to be returned,
            for html in summary[i]:         # <p>'s include <span>'s, beautiful soup gets rid of them
                rettext += html
            soup = BeautifulSoup(rettext, features="lxml")

            self.urltophoto = photoUrls[i]  # get the current photo url
            self.url = urls[i]              # get the current url

            if self.url[0] != 'h':          # urls that start with https are external links I don't like them.
                self.summary = soup.get_text()

                yield scrapy.Request(response.urljoin(self.url), self.parse_news)


    def parse_news(self, response):
        ret = response.css('div.articlePage p').getall()

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

        yield{
            "article" : article,
            'summary': self.summary,
            "url": self.url,
            "photo": self.urltophoto
        }