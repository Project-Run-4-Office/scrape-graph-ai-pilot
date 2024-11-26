import os
from dotenv import load_dotenv
from smartScrapeGraph import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info

load_dotenv()

openai_key = os.getenv("OPENAI_APIKEY")

graph_config = {
   "llm": {
      "api_key": openai_key,
      "model": "openai/gpt-4o",
   },
   "verbose": True,
   "headless": True,
}

# ************************************************
# Create the SmartScraperGraph instance and run it
# ************************************************

smart_scraper_graph = SmartScraperGraph(
   prompt="List me all the projects with their description.",
   # also accepts a string with the already downloaded HTML code
   source="https://perinim.github.io/projects/",
   config=graph_config
)

result = smart_scraper_graph.run()
print(result)