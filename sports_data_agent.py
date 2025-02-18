"""
PLACEHOLDER - To be modified
"""

import os
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

CHAT_MODEL = "gpt-4o"

@tool
def search_ticker(company_name: str) -> str:
    """
    Searches for the stock ticker symbol of a given company using DuckDuckGo.
    It parses search results specifically checking for entries from MarketWatch.
    """
    search = DuckDuckGoSearchRun()
    search_results = search.run(company_name)
    if isinstance(search_results, str):
        return search_results
    else:
        for result in search_results:
            try:
                if result["title"] == "Stock Ticker Symbol Lookup - MarketWatch":
                    return result["description"].split(" ")[-1]
            except:
                print('The result is not a dictionary. The result is {result}'.format(result=result))
        return "No ticker found"

if __name__ == '__main__':
    llm = ChatOpenAI(model=CHAT_MODEL)
    agent = initialize_agent(
        tools=[search_ticker],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    output = agent.run("what is the ticker of Genentech? If you cannot find it please return the ticker of its parent company.")
    print(output)