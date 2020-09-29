import scrapy
import re
from scrapy.selector import Selector
from items import BasicCrawlerItem
from scrapy.http import Request

class mySpider(scrapy.Spider):
    name = "skrap"
    start_urls = ['https://forum.hegnar.no/archive']

    def parse(self, response):
        hxs = Selector(response)
        
        # Variables for xpaths for HTML points of interest on the forum
        tittel = hxs.xpath("//a[@class='tittel']/text()").extract()
        ticker = hxs.xpath("//div[@class='postTicker']//a/text()").extract_first()
        username = hxs.xpath("//a[@class='registeredUser']/text()").extract_first()
        date = hxs.xpath("//div[@class='date']/text()").extract()
        comments = hxs.xpath("//div[@id='MainContent']//div[starts-with(name(), 'post')]//div[@class='postBody']//h2/text()").extract()
        # Save URLs and avoid duplicates from same post
        response_url = [] 

        for tittel in tittel:
            if not response.url in response_url: # Qualifier to avoid all but the first post in the thread
                collect = BasicCrawlerItem()
                collect['location_url'] = response.url
                collect['title'] = tittel
                collect['username'] = username
                collect['ticker'] = ticker
                collect['date'] = date
                collect['comments'] = comments
                #tit['link'] = link
                response_url.append(response.url)
                #tick.append(ticker)
                yield collect

        # Visits links to threads on forum
        links = hxs.xpath("//div[@id='main']//td[@class='colFiller']//a[@class='thread']/@href").extract()
        visited_links = []
        link_validator = re.compile("^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
        for link in links:
            if link_validator.match(link) and not link in visited_links:
                visited_links.append(link)
                yield Request(link, self.parse)
            else:
                full_url = response.urljoin(link)
                visited_links.append(response.url)
                yield Request(full_url, self.parse)