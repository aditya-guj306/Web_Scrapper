import scrapy
from w3lib.html import remove_tags
from bs4 import BeautifulSoup
import os,time
from groq import Groq
from typing import List, Optional
import json
from pydantic import BaseModel
import pandas as pd
import csv

GROQ_API_KEY="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"
client = Groq( api_key=GROQ_API_KEY,)

lis=[]
class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    start_urls = ["https://www.homedepot.com/p/Murray-MT100-42-in-13-5-HP-500cc-E1350-Series-Briggs-and-Stratton-Engine-6-Speed-Manual-Gas-Riding-Lawn-Tractor-Mower-MYT4213500/317475333",
                  "https://www.homedepot.com/p/Cub-Cadet-XT1-Enduro-LT-46-in-22-HP-V-Twin-Kohler-7000-Series-Engine-Hydrostatic-Drive-Gas-Riding-Lawn-Tractor-LT46/318885541",
                  "https://www.homedepot.com/p/Murray-21-in-140-cc-Briggs-and-Stratton-Walk-Behind-Gas-Push-Lawn-Mower-with-Height-Adjustment-and-Prime-N-Pull-Start-MNA152702/314250724",
                  "https://www.homedepot.com/p/Yard-Machines-20-in-125-cc-OHV-Briggs-and-Stratton-Gas-Walk-Behind-Push-Mower-11A-02BT729/300193832",
                  "https://www.homedepot.com/p/Powercare-20-oz-SAE-30-Tractor-and-Lawn-Mower-Engine-Oil-AP20300A/202564515"]

    def parse(self, response):
        plain_text = remove_tags(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        for data in soup(['style', 'script']):
            data.decompose()
 
   
        plain_text= ' '.join(soup.stripped_strings)
        time.sleep(3)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": plain_text,
                    
                },
                {
                    "role": "user",
                    "content": "productname: [str] ,price: [int] ,details: [str], specifications: [str] follow this schema and give output in json format"
                }
            ],
            model="mixtral-8x7b-32768",
            
        )
        # print(chat_completion.choices[0].message.content)
        
        entry = chat_completion.choices[0].message.content
        lis.append(entry)
        print(lis)

    
    # with open("data.json", mode='a', encoding='utf-8') as feedsjson:
    #     feedsjson.write(json.dumps(lis, indent=2))
    #     feedsjson.close()
    #     with open("data.csv", mode='w', newline='', encoding='utf-8') as csvfile:
    #         fieldnames = ['productname', 'price', 'details', 'specifications']
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         writer.writeheader()
    #         for entry in lis:
    #             writer.writerow(entry)
                