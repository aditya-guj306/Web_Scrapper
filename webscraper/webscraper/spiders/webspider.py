import scrapy
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_transformers import Html2TextTransformer
from w3lib.html import remove_tags
from bs4 import BeautifulSoup
import os,time
from groq import Groq
from typing import List, Optional
import json
from pydantic import BaseModel

GROQ_API_KEY="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"
client = Groq( api_key=GROQ_API_KEY,)


class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    # allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://www.homedepot.com/p/Murray-MT100-42-in-13-5-HP-500cc-E1350-Series-Briggs-and-Stratton-Engine-6-Speed-Manual-Gas-Riding-Lawn-Tractor-Mower-MYT4213500/317475333",
                  "https://www.homedepot.com/p/Cub-Cadet-XT1-Enduro-LT-46-in-22-HP-V-Twin-Kohler-7000-Series-Engine-Hydrostatic-Drive-Gas-Riding-Lawn-Tractor-LT46/318885541",
                  "https://www.homedepot.com/p/Murray-21-in-140-cc-Briggs-and-Stratton-Walk-Behind-Gas-Push-Lawn-Mower-with-Height-Adjustment-and-Prime-N-Pull-Start-MNA152702/314250724",
                  "https://www.homedepot.com/p/Yard-Machines-20-in-125-cc-OHV-Briggs-and-Stratton-Gas-Walk-Behind-Push-Mower-11A-02BT729/300193832",
                  "https://www.homedepot.com/p/Powercare-20-oz-SAE-30-Tractor-and-Lawn-Mower-Engine-Oil-AP20300A/202564515"]

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
        # f = open('file.txt', 'a', encoding='utf-8')
        # line=f.readline(plain_text)
        # while line!='':
        #     filelines.append(line)
        # f.close()
        # f.append(plain_text)
        # print(plain_text)
        time.sleep(3)
        with open("data.json", mode='a', encoding='utf-8') as f:
            json.dump([], f)
        

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": plain_text,
                    
                },
                {
                    "role": "user",
                    "content": "product_name: [str] ,price: [str] ,details: [str], specifications: [str] follow this schema and give output in json format"
                }
            ],
            model="mixtral-8x7b-32768",
            
        )
        print(chat_completion.choices[0].message.content)
        # chat_completion = client.chat.completions.create(
        #     messages=[
        #         {
        #           "role": "system",
        #           "content": plain_text,
        
        #         },
        #         {
        #          "role": "user",
        #          "content": "What is the name of the product?,what is price of the product?,What are the details of the product?,what are the specifications?",
        #          },
        #      ],
        #     model="mixtral-8x7b-32768",
        #     temperature=0,
        #     stream=False,
        #     response_format={type: "json_object"},
        # )
        # print (chat_completion.choices[0].message.content)
        with open("data.json", mode='a', encoding='utf-8') as feedsjson:
            entry = chat_completion.choices[0].message.content
            json.dump(entry, feedsjson)
        # chat_completion = client.chat.completions.create(
        #     messages=[
        #     {
        #         "role": "system",
        #         "content": plain_text,
        #     },
        #     {
        #         "role": "user",
        #         "content": "What is the name of the product?,what is price of the product?,What are the details of the product?,what are the specifications?",
        #     }
        #     ],
        #     model="mixtral-8x7b-32768",
        #     temperature=0,
        #     stream=False,
        #     response_format={"type":"json_object"},
        # )

        # print(chat_completion.choices[0].message.content)
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