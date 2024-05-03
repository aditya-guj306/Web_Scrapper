# import scrapy
# from w3lib.html import remove_tags
# from bs4 import BeautifulSoup
# import os,time
# from groq import Groq
# from typing import List, Optional
# import json
# from pydantic import BaseModel
# import pandas as pd
# import csv

# GROQ_API_KEY="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"
# client = Groq( api_key=GROQ_API_KEY)

# lis=[]
# class WebspiderSpider(scrapy.Spider):
#     name = "webspider"
#     start_urls = ["https://www.homedepot.com/p/Murray-MT100-42-in-13-5-HP-500cc-E1350-Series-Briggs-and-Stratton-Engine-6-Speed-Manual-Gas-Riding-Lawn-Tractor-Mower-MYT4213500/317475333",
#                   "https://www.homedepot.com/p/Cub-Cadet-XT1-Enduro-LT-46-in-22-HP-V-Twin-Kohler-7000-Series-Engine-Hydrostatic-Drive-Gas-Riding-Lawn-Tractor-LT46/318885541",
#                   "https://www.homedepot.com/p/Murray-21-in-140-cc-Briggs-and-Stratton-Walk-Behind-Gas-Push-Lawn-Mower-with-Height-Adjustment-and-Prime-N-Pull-Start-MNA152702/314250724",
#                   "https://www.homedepot.com/p/Yard-Machines-20-in-125-cc-OHV-Briggs-and-Stratton-Gas-Walk-Behind-Push-Mower-11A-02BT729/300193832",
#                   "https://www.homedepot.com/p/Powercare-20-oz-SAE-30-Tractor-and-Lawn-Mower-Engine-Oil-AP20300A/202564515"]

#     def parse(self, response):
#         plain_text = remove_tags(response.text)
#         soup = BeautifulSoup(response.text, "html.parser")
#         for data in soup(['style', 'script']):
#             data.decompose()
 
   
#         plain_text= ' '.join(soup.stripped_strings)
#         time.sleep(3)
        
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": plain_text,
                    
#                 },
#                 {
#                     "role": "user",
#                     "content": "productname: [str] ,price: [int] ,details: [str], specifications: [str] follow this schema and give output in json format"
#                 }
#             ],
#             model="mixtral-8x7b-32768",
            
#         )
#         # print(chat_completion.choices[0].message.content)
        
#         entry = chat_completion.choices[0].message.content
#         print(entry)
#         lis.append(entry)

#     def closed(self, reason):
#         # Save the scraped data to a JSON file
#         with open("data.json", mode='w', encoding='utf-8') as json_file:
#             json.dump(lis, json_file, indent=4)
#             print("Data has been saved to data.json")
#         # Save the scraped data to a CSV file
#         with open("data.json", 'r') as j:
#             x = json.loads(j.read())
#             pd.DataFrame({"ProductName":x[0],
#                 "Price":x[1],
#                 "Details":x[2],
#                 "Specifications":x[3]},
#                 index=False).to_csv("data.csv", mode='a', header=False)


import scrapy
from w3lib.html import remove_tags
from bs4 import BeautifulSoup
import os
import time
from groq import Groq
import json
import pandas as pd

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    start_urls = [
        "https://shop.lululemon.com/p/hats/Trucker-Hat/_/prod11020363?color=27597",
        "https://www.potterybarn.com/products/delaney-marble-floor-lamp/?pkey=cfloor-lamps",
        "https://www.bjs.com/product/garmin-vivoactive-5-gps-smartwatch/3000000000005027783",
        "https://www.homedepot.com/p/Murray-MT100-42-in-13-5-HP-500cc-E1350-Series-Briggs-and-Stratton-Engine-6-Speed-Manual-Gas-Riding-Lawn-Tractor-Mower-MYT4213500/317475333",
        "https://www.homedepot.com/p/Cub-Cadet-XT1-Enduro-LT-46-in-22-HP-V-Twin-Kohler-7000-Series-Engine-Hydrostatic-Drive-Gas-Riding-Lawn-Tractor-LT46/318885541",
        "https://www.homedepot.com/p/Murray-21-in-140-cc-Briggs-and-Stratton-Walk-Behind-Gas-Push-Lawn-Mower-with-Height-Adjustment-and-Prime-N-Pull-Start-MNA152702/314250724",
        "https://www.homedepot.com/p/Yard-Machines-20-in-125-cc-OHV-Briggs-and-Stratton-Gas-Walk-Behind-Push-Mower-11A-02BT729/300193832",
        "https://www.homedepot.com/p/Powercare-20-oz-SAE-30-Tractor-and-Lawn-Mower-Engine-Oil-AP20300A/202564515"
    ]

    def parse(self, response):
        plain_text = remove_tags(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        for data in soup(['style', 'script']):
            data.decompose()

        plain_text = ' '.join(soup.stripped_strings)
        time.sleep(3)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": plain_text,
                },
                {
                    "role": "user",
                    "content": "productname: [str] ,price: [float] ,details: [str], specifications: [str] follow this schema and give output in json format and always consider price that are followed or precedded by a currency symbol"
                }
            ],
            model="mixtral-8x7b-32768",
        )

        entry = chat_completion.choices[0].message.content
        url=response.url
        self.save_to_csv(entry,url)
        self.save_to_json(entry,url)

    def save_to_csv(self, groq_response,url):
        if os.path.exists("data.csv"):
            df = pd.read_csv("data.csv")
        else:
            df = pd.DataFrame(columns=["productname", "price", "details", "specifications","url"])

        groq_json = json.loads(groq_response)
        groq_json["url"] = url

        groq_df = pd.DataFrame(groq_json, index=[0])
        df = pd.concat([df, groq_df], ignore_index=True)
        df.to_csv("data.csv", index=False)

        print("Data appended to data.csv")
    
    def save_to_json(self, groq_response, url):
        if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
            with open("data.json", "r") as json_file:
                data = json.load(json_file)
        else:
            data = []
        groq_json = json.loads(groq_response)

        groq_json["url"] = url

        data.append(groq_json)

        with open("data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        print("Data appended to data.json")


