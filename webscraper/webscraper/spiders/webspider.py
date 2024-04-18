# import scrapy


# class WebspiderSpider(scrapy.Spider):
#     name = "webspider"
#     # allowed_domains = ["books.toscrape.com"]
#     start_urls = ["https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"]

#     def parse(self, response):
#         print(response.text)
        # items=response.css('ul .product-summary')
        
        # for item in items:
        #     yield{
        #         'Product Name':item.css('h2 .product-title::text').get(),
        #         # 'Price':item.css('.product_price .price_color::text').get(),
        #         # 'url':item.css('h3 a').attrib['href'],
        #         'details':item.css('div .value::text').get(),
        #     }


import scrapy
from w3lib.html import remove_tags
from langchain.text_splitter import RecursiveCharactertextSplitter
from langchain.document_transformers import Html2TextTransformer
import openai,sys
class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    start_urls = ["https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"]
    # Add your allowed domains and start URLs here

    def parse(self, response):
        # Extract the HTML content
        html_content = response.css("body").get()

        # Remove HTML tags using w3lib.html.remove_tags
        plain_text = remove_tags(html_content)

        # Yield the extracted plain text
        yield {
            'url': response.url,
            'plain_text': plain_text,
        }