from samplePlan import scrape_sample_plan
from langchain_core.tools import tool
from langchain_core.agents import create_tool_calling_agent
from langchain_openai import ChatOpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-5-nano", temperature=0.0)

with open("test_student.json", "r") as f:
    student_profile = json.load(f)

@tool
def scraper_tool(url):
    return scrape_sample_plan(url)

sample_plan_urls = [
    "https://www.truman.edu/fouryearplan/computer-science-bs/",
    "https://www.truman.edu/fouryearplan/accounting-major/",
    "https://www.truman.edu/fouryearplan/agricultural-science-business-track/",
    "https://www.truman.edu/fouryearplan/agricultural-science-pre-education-track/",
    "https://www.truman.edu/fouryearplan/agricultural-science-science-track/",
    "https://www.truman.edu/fouryearplan/history-bsba/",
    "https://www.truman.edu/fouryearplan/music-ba-pre-certification-instrumental/"
]

prompt = f"""
You are an academic advisor AI agent. Your goal is to help the student plan their courses. 
You can reason step by step, ask for data if needed, and pick courses dynamically.

Rules:
1. Check the student's profile and remaining requirements.
2. You can call the tool `scrape_sample_plan` to fetch courses from a `sample_plan_urls` if you need more courses for a missing Dialogues perspective.
3. Only recommend courses:
    - Not already completed
    - Offered in their plan's 1st semester or at most 2nd semester
    - Matching missing requirements or user interest
4. Explain your reasoning step by step.
5. Output recommended courses in JSON format:
[
  {"code": "...", "name": "...", "credits": ..., "perspective": "..."}
]"""

tools = [scraper_tool]

agent = create_tool_calling_agent(tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)

user_input = f"""
Student profile:
{json.dumps(student_profile, indent=2)}

Available sample plan URLs:
{json.dumps(sample_plan_urls, indent=2)}

Task: Recommend courses for the next semester. If you need example courses for a perspective, call:
scrape_sample_plan("<url>") with the chosen URL. Only pick courses that are in semester 1 or 2 of the scraped plan.
Explain your reasoning step-by-step and produce JSON recommendations.
"""

result_text = agent.run(user_input)
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(result_text)
print(result_text)
