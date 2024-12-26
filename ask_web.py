#------------------------------------
# 26.12.2024
# -----------------------------------

from tavily import TavilyClient

import os 
from dotenv import load_dotenv
load_dotenv()

class WebSearch:
    def __init__(self):
        self.tavilyClient = TavilyClient(api_key=os.environ.get('TAVILY_API_KEY_PRIVAT'))
        
    def search(self, query: str = "", score: float = 0.5, limit: int = 10) -> list:
        results: list = []
        try:
            results_list = self.tavilyClient.search(
                query=query,
                # topic="news",
                max_results=limit,
                )
        except:
            return results
        for result in results_list['results']:
            if result['score'] > score:
                results.append(result)
        return results
    
    def search_context(self, query: str = "", score: float = 0.5, limit: int = 10) -> str:
        context = self.tavilyClient.get_search_context(
            query=query,
            # topic="News",
            max_results=limit,
            )
        return context

    # @staticmethod
    # def print_results(cursor: list) -> None:
    #     if not cursor:
    #         print("Keine Artikel gefunden.")
    #     for item in cursor:
    #         print(f"[{str(item['datum'])[:10]}] {item['titel'][:70]}")