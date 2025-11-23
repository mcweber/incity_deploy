# ------------------------------------
# 21.11.2025 added included_domains
# 21.11.2025 modified dotenv path
# -----------------------------------

import os
from dotenv import load_dotenv
from tavily import TavilyClient


class WebSearch:
    def __init__(self):
        load_dotenv(os.path.expanduser("~/.env"))
        self.tavilyClient = TavilyClient(api_key=os.environ["TAVILY_API_KEY_PRIVAT"])

    def search(self, query:str="", domains:str="", score:float=0.5, limit:int=10) -> list:
        results: list = []
        domains_list = domains.split(" ") if domains else []
        try:
            results_list = self.tavilyClient.search(
                query=query,
                include_domains=domains_list,
                # topic="news",
                max_results=limit,
            )
        except:
            return results

        for result in results_list["results"]:
            if result["score"] > score:
                results.append(result)

        return results

    def search_context(
        self, query:str="", domains:str="", score:float=0.5, limit:int=10
    ) -> str:
        domains_list = domains.split(" ") if domains else []
        context = self.tavilyClient.get_search_context(
            query=query,
            include_domains=domains_list,
            topic="news",
            max_results=limit,
        )
        return context

    # @staticmethod
    # def print_results(cursor: list) -> None:
    #     if not cursor:
    #         print("Keine Artikel gefunden.")
    #     for item in cursor:
    #         print(f"[{str(item['datum'])[:10]}] {item['titel'][:70]}")
