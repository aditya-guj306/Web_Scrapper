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
    prompt="extract name of the product, its price and details",
    # source="https://www.webtoons.com/en/drama/the-horizon/episode-2/viewer?title_no=3141&episode_no=2",
    source="https://shop.lululemon.com/p/hats/Trucker-Hat/_/prod11020363?color=27597",
    config=graph_config
)

result = smart_scraper_graph.run()
print(result)