import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]

    def parse(self, response):
        products = response.css('div.ui-search-results ui-search-results--without-disclaimer')

        for product in products:

            yield {
                'brand': product.css("span.poly-component__brand::text").get()
            }
        


        pass
