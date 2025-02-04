import scrapy
from selenium import webdriver

class PelandoSpider(scrapy.Spider):
    name = "pelando"
    allowed_domains = ["www.pelando.com.br"]
    start_urls = ["https://www.pelando.com.br/busca/tenis-masculino"]

    def parse(self, response):
        yield {'pelando':response.css('div.sc-ia-dotI.grhpDz').get()
               }
       


        pass
