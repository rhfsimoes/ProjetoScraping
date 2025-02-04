import scrapy


class PelandoSpider(scrapy.Spider):
    name = "pelando"
    allowed_domains = ["www.pelando.com.br"]
    start_urls = ["https://www.pelando.com.br/busca/tenis-masculino"]

    def parse(self, response):
        pass
