"""
PLACEHOLDER - To be modified
"""

import os
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun, tool

@tool
def search_ticker(company_name: str) -> str:
    """
    Searches for the stock ticker symbol of a given company using DuckDuckGo.
    It parses search results specifically checking for entries from MarketWatch.
    """
    search = DuckDuckGoSearchRun()
    search_results = search.run(company_name)
    for result in search_results:
        if result["title"] == "Stock Ticker Symbol Lookup - MarketWatch":
            return result["description"].split(" ")[-1]
    return "No ticker found"


llm = ChatOpenAI(temperature=0.0)
tools = load_tools(["search_ticker"], llm=llm)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
output = agent.run("what is the ticker of Amazon")
print(output)

import os
from openai import OpenAI, RateLimitError, Timeout, APIError, APIConnectionError, OpenAIError
from dotenv import load_dotenv
from collections import deque

from datetime import datetime
from functools import lru_cache

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))



# try:
#     # Now you can use the 'client' object to interact with the OpenAI API
#     # For example, to create a chat completion:
#     response = client.chat.completions.create(
#       model="gpt-4o",
#       messages=[
#         {
#           "role": "user",
#           "content": [
#             {
#               "type": "text",
#               "text": "I am facing an issue where I cannot set up a Teradata database using tdvm-init on a Linux virtual machine running on a VMWare ESXi server. The process keeps getting stuck on \"Info: Starting TD Put Process to configure Database.\" and then eventually crashes. Can you help me?"
#             }
#           ]
#         }
#       ],
#       response_format={
#         "type": "text"
#       },
#       temperature=0.5,
#       max_completion_tokens=2048,
#       top_p=1,
#       frequency_penalty=0,
#       presence_penalty=0
#     )
#     print(response.choices[0].message.content)
# except openai.AuthenticationError as e:
#     print(f"Authentication error: {e}")
# except openai.APIConnectionError as e:
#     print(f"API connection error: {e}")
# except openai.RateLimitError as e:
#     print(f"Rate limit error: {e}")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")



# Inspired by Stan Chen's code: https://github.com/stancsz/chatgpt
CHAT_MODEL = "gpt-4o"
# PROMPT = """Your name is Kim. A kind and friendly AI assistant that answers in \
#     a short and concise answer. Give short step-by-step reasoning if required."""
PROMPT = """
  Your name is Roger. A kind and friendly AI assistant who provides recommendations for \
  coworkers. Please provide your responses in medium length paragraphs that express your
  gratitutde for the recommendation recipient.
"""

class Chat:
    def __init__(self, converstion_limit: int = 8):

        # number of chats to remember
        self.messages_queue = deque(maxlen=converstion_limit)

    @lru_cache(maxsize=518)
    def chat(self, message: str) -> str:
        self.messages_queue.append({"role": "user", "content": message})

        try:
            prompty = {
                "role": "user",
                "content": [{"type": "text", "text": f"{PROMPT} Today is {datetime.now(): %A %d %B %Y %H:%M}"}],
            }
            # response = openai.ChatCompletion.create(
            response = client.chat.completions.create(
                model=CHAT_MODEL, messages=[prompty, *self.messages_queue],
                response_format={
                  "type": "text"
                },
                temperature=0.5,
                max_completion_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # reply = response["choices"][0]["message"].content
            reply = response.choices[0].message.content

            self.messages_queue.append({"role": "assistant", "content": reply})
        except RateLimitError:
            reply = "I am currently overloaded with other requests."

        return reply

if __name__ == '__main__':
  # create chat obj
  chat_limit = 0
  chatter = Chat()
  while chat_limit <= 8:
    user_input = input("Enter your question: ")
    reply = chatter.chat(user_input)
    print(reply)
    chat_limit += 1
