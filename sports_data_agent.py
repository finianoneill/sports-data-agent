"""
NBA Statistics Web Scraper
==========================

This script creates an autonomous agent that uses LangChain and OpenAI to gather, 
process, and store up-to-date NBA statistics from web searches.

Functionality:
-------------
1. Uses DuckDuckGo search to find the latest NBA statistics and game results
2. Leverages GPT-4o to extract structured data from search results
3. Collects multiple statistical categories (points, rebounds, assists, etc.)
4. Processes data into structured JSON format
5. Saves results to both JSON and CSV files for later analysis
6. Provides an interactive command-line interface for viewing results

Key Components:
--------------
- LLM Integration: Uses ChatOpenAI (GPT-4o) for natural language processing
- Search Tool: DuckDuckGoSearchRun for retrieving web search results
- Data Extraction: Custom prompt template for parsing unstructured search results
- Data Storage: Saves compiled statistics to local filesystem
- User Interface: Interactive CLI for data exploration

Usage:
------
Run the script directly to collect the latest NBA statistics:
$ python sports_data_agent.py

Once running, use the interactive prompt to:
- view [stat_type]: Display leaders for a specific statistical category
- refresh: Fetch updated statistics
- exit: Terminate the program

Dependencies:
------------
- langchain and langchain_openai: For LLM integration and agent creation
- langchain_community.tools: For web search capabilities
- pandas: For data manipulation and CSV export
- python-dotenv: For environment variable management

Note: Requires an OpenAI API key stored in an .env file.
"""

# NBA Stats Web Scraper using Langchain and OpenAI

import os
import json
import pandas as pd
from datetime import datetime
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun

from dotenv import load_dotenv

load_dotenv()

CHAT_MODEL = "gpt-4o"

# Initialize the language model
llm = ChatOpenAI(temperature=0, model_name=CHAT_MODEL)

# Initialize web search
search = DuckDuckGoSearchRun()

# Create a search tool
search_tool = Tool(
    name="DuckDuckGo Search",
    description="Search using DuckDuckGo for recent NBA statistics and scores",
    func=search.run
)

# Define the statistics we want to collect
stats_categories = [
    "points",
    "rebounds",
    "assists",
    "steals",
    "blocks",
    "field_goal_percentage",
    "three_point_percentage",
    "free_throw_percentage",
    "plus_minus"
]

# Create a prompt template for extracting structured data
extract_stats_template = """
You are tasked with extracting NBA statistics from search results.
Search Results: {search_results}

Please extract the following statistics for the most recent games:
1. Team names
2. Final scores
3. Date of the game
4. Leading scorers and their points
5. Any {stat_category} leaders mentioned

Return the data in a structured JSON format with game date, teams, scores, and player statistics.
Only include factual information directly from the search results. If certain statistics aren't 
available, omit them rather than making assumptions. I repeat!!! ONLY RETURN THE JSON NO EXTRANNEOUS STRING!!
"""

extract_stats_prompt = PromptTemplate(
    input_variables=["search_results", "stat_category"],
    template=extract_stats_template
)

extract_stats_chain = LLMChain(
    llm=llm,
    prompt=extract_stats_prompt
)

def parse_llm_json_return_string(input_string: str):
    """
    Helper function to remove extraneous text.
    """
    return input_string.replace("`", "").replace("json", "")

# Main function to fetch NBA statistics
def fetch_nba_stats():
    all_stats = {}
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create a directory for storing the data
    os.makedirs("nba_stats", exist_ok=True)
    
    # Fetch general scores first
    query = "latest NBA scores results today"
    search_results = search_tool.run(query)
    
    # Extract general game information
    extraction_result = extract_stats_chain.run(
        search_results=search_results,
        stat_category="general"
    )
    extraction_result = parse_llm_json_return_string(input_string=extraction_result)
    
    try:
        games_data = json.loads(extraction_result)
        all_stats["games"] = games_data
    except json.JSONDecodeError as j_error:
        print("Error parsing general game data. Continuing with individual stats...")
        print('-' * 50)
        print(f"ERROR: {j_error}")
        print(f"EXTRACTION RESULT: {extraction_result}")
        print('-' * 50)
        all_stats["games"] = []
    
    # Fetch specific statistics for each category
    for stat in stats_categories:
        query = f"latest NBA {stat} leaders statistics today"
        search_results = search_tool.run(query)
        
        extraction_result = extract_stats_chain.run(
            search_results=search_results,
            stat_category=stat
        )
        extraction_result = parse_llm_json_return_string(input_string=extraction_result)
        
        try:
            stat_data = json.loads(extraction_result)
            all_stats[stat] = stat_data
        except json.JSONDecodeError as j_error:
            print(f"Error parsing {stat} data. Skipping this category.")
            print('-' * 50)
            print(f"ERROR: {j_error}")
            print(f"EXTRACTION RESULT: {extraction_result}")
            print('-' * 50)
            all_stats[stat] = []
    
    # Save the compiled data
    with open(f"nba_stats/nba_stats_{today}.json", "w") as f:
        json.dump(all_stats, f, indent=4)
    
    # Create a simple CSV for points leaders
    if "points" in all_stats and all_stats["points"]:
        try:
            points_df = pd.DataFrame(all_stats["points"])
            points_df.to_csv(f"nba_stats/points_leaders_{today}.csv", index=False)
        except Exception as e:
            print(f"Error creating CSV for points leaders: {e}")
    
    return all_stats

# Function to display recent results
def display_recent_results(stats):
    if "games" in stats and stats["games"]:
        print("\n===== RECENT NBA GAME RESULTS =====")
        for game in stats["games"]:
            print(f"\n{game['date']} - {game['home_team']} vs {game['away_team']}")
            print(f"Score: {game['home_score']} - {game['away_score']}")
            if "leading_scorer" in game:
                print(f"Leading Scorer: {game['leading_scorer']}")
    else:
        print("No recent game data available")

# Main execution
if __name__ == "__main__":
    print("Fetching latest NBA statistics...")
    stats = fetch_nba_stats()
    display_recent_results(stats)
    print(f"\nAll statistics saved to nba_stats directory")
    
    # Optionally add interactive mode to query specific stats
    while True:
        action = input("\nWhat would you like to do? (view [stat_type], refresh, exit): ")
        if action.lower() == "exit":
            break
        elif action.lower() == "refresh":
            stats = fetch_nba_stats()
            display_recent_results(stats)
        elif action.lower().startswith("view "):
            stat_type = action.lower().replace("view ", "")
            if stat_type in stats:
                print(f"\n===== {stat_type.upper()} LEADERS =====")
                for item in stats[stat_type]:
                    print(json.dumps(item, indent=2))
            else:
                print(f"No data available for {stat_type}")