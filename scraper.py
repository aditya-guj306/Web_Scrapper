# from scrapegraphai.graphs import SmartScraperGraph
# from langchain_community.document_loaders import AsyncChromiumLoader
import nest_asyncio
nest_asyncio.apply()
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info

groq_key = "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"

graph_config = {
    "llm": {
        "model": "groq/llama3-8b-8192",
        "api_key": groq_key,
        "temperature": 0
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "temperature": 0,
        "base_url": "http://localhost:11434", 
    },
    "headless": False
}

smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the quotes",
    source="https://quotes.toscrape.com/",
    config=graph_config
)

result = smart_scraper_graph.run()
print(result)