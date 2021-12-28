import scrapy

class WhiskeyscrapeSpider(scrapy.Spider):
    name = 'whisky'
    start_urls = ['https://www.whiskyshop.com/scotch-whisky/all']

    def parse(self, response):
        for products in response.css('div.product.details.product-item-details'): 
            try:
                yield {
                    'name': products.css('a.product-item-link::text').get(),
                    'price': products.css('span.price::text').get().replace('£', ''),
                    'link': response.css('a.product-item-link').attrib['href']
                }
            except:
                yield {
                    'name': products.css('a.product-item-link::text').get(),
                    'price': 'Sold Out',
                    'link': response.css('a.product-item-link').attrib['href']
                }
                
        next_page = response.css('a.action.next').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

