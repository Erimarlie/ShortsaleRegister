import scrapy
import re
#from bs4 import BeautifulSoup
from scrapy.selector import Selector
from items import BasicCrawlerItem
from scrapy.http import Request

class mySpider(scrapy.Spider):
    name = "skraper"
    #start_urls = ['https://quotes.hegnar.no/kurs.php']
    start_urls = ['https://investor.dn.no/#!/Kurser/Aksjer/']

    def parse(self, response):
        hxs = Selector(response)
        #soup = BeautifulSoup(self.start_urls, 'html.parser')

        # Variables for xpaths for HTML points of interest on the forum
        divs = hxs.xpath('//table[@class="table-static kurser-table"]')
        navn = hxs.xpath('//tr[@class="ng-scope"]/td[@class="hide-text-overflow"]/a')
        #divs = hxs.xpath('//table[@id="updatetable1"]').extract()
        #trows = hxs.xpath('//table[@id="updatetable1"]/tr').extract()
        #navn = hxs.xpath('//td[@class="left"]/a/text()').extract()
        #ticker = hxs.xpath('//td[@class="left"][2]/text()').extract()
        #sektor = hxs.xpath('//td[@id="dninvestor-content"]/div[1]/div/div[4]/table/tbody/tr[1]/td[12]').extract()
        ## Save URLs and avoid duplicates from same post
        #response_url = []
        i = 0

        for x in divs:
            collect = BasicCrawlerItem()
            collect['title'] = navn
            collect['ticker'] = ticker
            collect['sektor'] = sektor
            #collect['location_url'] = response.url
            #collect['username'] = username
            #collect['date'] = date
            #collect['comments'] = comments
            #response_url.append(response.url)
            yield collect
            i += 1

        print(i)

        # Visits links to threads on forum
        #links = hxs.xpath("//div[@id='main']//td[@class='colFiller']//a[@class='thread']/@href").extract()
        #visited_links = []
        #link_validator = re.compile("^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
        #for link in links:
        #    if link_validator.match(link) and not link in visited_links:
        #        visited_links.append(link)
        #        yield Request(link, self.parse)
        #    else:
        #        full_url = response.urljoin(link)
        #        visited_links.append(response.url)
        #        yield Request(full_url, self.parse)