
#https://plato.stanford.edu/contents.html
import scrapy
from bs4 import BeautifulSoup

class MainSpider(scrapy.Spider):
    name = "main"
    custom_settings = {
        'DOWNLOAD_DELAY': .5  # Set the delay to 1 second
    }
    def start_requests(self):
        urls = [
            "https://plato.stanford.edu/contents.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        article_set = set()
        list_items = response.xpath("//body/div[@id='container']/div[@id='content']//ul//li").getall()
        for list_item in list_items:
            list_item_soup = BeautifulSoup(list_item, 'html.parser')
            a = list_item_soup.a
            ul = list_item_soup.ul
            if a is not None:
                text = list_item_soup.getText()
                if "— see" in text:
                    continue
                else:
                    if list_item_soup.a is not None:
                        article_set.add(list_item_soup.a.get("href"))
                #check to see if --see also;
            if ul is not None:
                #for each of the lis in ul.
                sub_list = ul('li')
                for sub_list_item in sub_list:
                    text = sub_list_item.getText()
                    if "— see" in text:
                        continue
                    else:
                        if sub_list_item.a is not None:
                            article_set.add(sub_list_item.a.get("href"))
        print(article_set)
        print(len(article_set))
        request_list = []
        for url in article_set:
            yield scrapy.Request("https://plato.stanford.edu/" + url, self.parse_article)

    def parse_article(self, response):
        print (response.url + " This is the URL for our article")
        related = response.xpath("//body/div[@id='container']/div[@id='content']/div[@id='article']/div[@id='article-content']/div[@id='aueditable']/div[@id='related-entries']/p").get()
        if related is not None:
            related = BeautifulSoup(related, 'html.parser')
            references = related.find_all('a')
            for reference in references:
                print(reference.get('href') + " \n ")
        yield None












