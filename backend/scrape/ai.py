from typing import List
import json
import random
import string
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from samplePlan import scrape_sample_plan

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

@tool
def scrape_sample_plan(url: str) -> json:
    """Scrape Truman's sample plan based on the URL provided. Parse and return a string of JSON"""
    return scrape_sample_plan(url)


TOOLS = [scrape_sample_plan]