import scrapy
from  bs4 import BeautifulSoup

class ExampleSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['coindesk.com',
                       'investing.com',
                       'coinmarketcap.com',
                       'yahoo.com',
                       'cryptonews.com']

    start_urls = ['https://www.investing.com/news/cryptocurrency-news']

    def parse(self, response):
        for link in response.css('div.largeTitle article a::attr(href)'):
            url = link.get()
            if url[0] != 'h':
                yield scrapy.Request(response.urljoin(url), self.parse_news)

        # for link in response.css('div.largeTitle article img::attr(data-src)'):
        #     yield {
        #         "image": link.get()
        #     }

    def parse_news(self, response):

        yield{
            "text" : response.css('div.articlePage p::text').getall()
        }

        #soup = BeautifulSoup(response.body, 'html.parser')
        #largeTitleContents = soup.select("div .largeTitle article")
        #print(largeTitleContents[0].find_all("a"))
        #yield {"url" : response.text}
