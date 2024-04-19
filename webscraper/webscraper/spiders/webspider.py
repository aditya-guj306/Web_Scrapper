import scrapy
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_transformers import Html2TextTransformer
from w3lib.html import remove_tags
from bs4 import BeautifulSoup


class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    # allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://www.acehardware.com/departments/tools/power-tools/cordless-drills","https://www.homedepot.com/p/Cub-Cadet-XT1-Enduro-LT-46-in-22-HP-V-Twin-Kohler-7000-Series-Engine-Hydrostatic-Drive-Gas-Riding-Lawn-Tractor-LT46/318885541"]

    def parse(self, response):
        # print(response.text)
        plain_text = remove_tags(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        for data in soup(['style', 'script']):
        # Remove tags
            data.decompose()
 
    # return data by retrieving the tag content
        plain_text= ' '.join(soup.stripped_strings)
        # tt=Html2TextTransformer()
        # doc=tt.transform_documents(response.text)
        # tc=RecursiveCharacterTextSplitter(())
        # slipt=tc.split_text((plain_text))
        f = open('file.txt', 'w', encoding='utf-8')
        f.write(plain_text)
        # print(slipt)
        # items=response.css('ul .product-summary')
        
        # for item in items:
        #     yield{
        #         'Product Name':item.css('h2 .product-title::text').get(),
        #         # 'Price':item.css('.product_price .price_color::text').get(),
        #         # 'url':item.css('h3 a').attrib['href'],
        #         'details':item.css('div .value::text').get(),
            # }


# import scrapy
# from w3lib.html import remove_tags
# from langchain.text_splitter import RecursiveCharactertextSplitter
# from langchain.document_transformers import Html2TextTransformer
# import openai,sys
# class WebspiderSpider(scrapy.Spider):
#     name = "webspider"
#     start_urls = ["https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"]
#     # Add your allowed domains and start URLs here

#     def parse(self, response):
#         # Extract the HTML content
#         html_content = response.css("body").get()

#         # Remove HTML tags using w3lib.html.remove_tags
#         plain_text = remove_tags(html_content)

#         # Yield the extracted plain text
#         yield {
#             'url': response.url,
#             'plain_text': plain_text,
#         }