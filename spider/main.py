#!/usr/bin/env python
from pymongo import MongoClient
from dragline.runner import main
from dragline.htmlparser import HtmlParser
from dragline.http import Request
import settings


class Spider:
    mydb = MongoClient(host ="localhost")["goodread"]
    
    def __init__(self, conf):
        self.name = "brainy"
        self.start = "https://www.goodreads.com/quotes"
        self.allowed_domains = ["www.goodreads.com"]
        self.conf = conf

    def parse(self,response):
        parser = HtmlParser(response)
        for url in parser.extract_urls('//a[@class="actionLinkLite serif"]'):
            dbname = url.split('/')[-1]
            yield Request(url,callback="parseCat",meta={'u':dbname})


    def parseCat(self, response):
        parser = HtmlParser(response)
        dbname= response.meta['u']
        if not  parser.xpath('//a[@class="next_page"]'):
            for i in parser.xpath('//div[@class="quoteText"]'):
                quote = i.text
                for j in i.iterfind('a'):
                    author=j.text
                self.mydb[dbname].insert({'quote':quote,'author':author})
        else:
            for i in parser.xpath('//div[@class="quoteText"]'):
                quote = i.text
                for j in i.iterfind('a'):
                    author=j.text
                self.mydb[dbname].insert({'quote':quote,'author':author})
            
            for url in parser.extract_urls('//a[@class="next_page"]'):
                yield Request(url,callback="parseCat",meta={'u':dbname})

if __name__ == '__main__':
    main(Spider, settings)
