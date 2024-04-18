from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import Html2TextTransformer
import openai,sys

url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
loader=AsyncChromiumLoader([url])
tt=Html2TextTransformer()
doc=tt.transform_documents(loader.load())
tc=RecursiveCharacterTextSplitter(())
slipt=tc.split_documents((doc))
print(slipt)
print(slipt[0].page_content)
# print(type(slipt))
# x=' '
# for item in slipt[0]:
#     x+=item
# print(x)
# print(type(x))

GROQ_API_KEY="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"

import os

from groq import Groq

client = Groq(
    api_key=GROQ_API_KEY,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": slipt[0].page_content,
        },
        {
            "role": "user",
            "content": "What is the name of the book?, what is price of the book?",
        }
    ],
    model="mixtral-8x7b-32768",
)

print(chat_completion.choices[0].message.content)