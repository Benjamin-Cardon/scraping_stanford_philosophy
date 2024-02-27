
#https://plato.stanford.edu/contents.html
import scrapy
from bs4 import BeautifulSoup

class MainSpider(scrapy.Spider):
    name = "main"
    def start_requests(self):
        urls = [
            "https://plato.stanford.edu/contents.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        article_urls = []
        list_items = response.xpath("//body/div[@id='container']/div[@id='content']//ul//li").getall()
        for list_item in list_items:
            list_item_soup = BeautifulSoup(list_item, 'html.parser')
            a = list_item_soup.a
            ul = list_item_soup.ul
            if a is not None:
                print(list_item_soup.getText())
                #check to see if --see also;
            if ul is not None:
                print("SubList")
                #for each of the lis in ul.







