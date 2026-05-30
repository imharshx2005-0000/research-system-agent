import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langgraph.prebuilt import create_react_agent

from tools import web_search, scrape_url

from langchain_groq import ChatGroq

# ==================================================
# LOAD ENV VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# LLM SETUP
# ==================================================




llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)
# ==================================================
# SEARCH AGENT
# ==================================================

def build_search_agent():

    return create_react_agent(
        model=llm,
        tools=[web_search]
    )


# ==================================================
# READER AGENT
# ==================================================

def build_reader_agent():

    return create_react_agent(
        model=llm,
        tools=[scrape_url]
    )


# ==================================================
# WRITER CHAIN
# ==================================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. "
        "Write clear, structured, and insightful reports."
    ),

    (
        "human",
        """
Write a detailed research report based on the information below.

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:

- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual, and professional.
"""
    ),
])


writer_chain = writer_prompt | llm | StrOutputParser()


# ==================================================
# CRITIC CHAIN
# ==================================================

critic_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        "You are a sharp and constructive research critic. "
        "Be honest and specific."
    ),

    (
        "human",
        """
Review the research report below and evaluate it strictly.

Report:
{report}

Respond in the exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One Line Verdict:
...
"""
    )

])


critic_chain = critic_prompt | llm | StrOutputParser()