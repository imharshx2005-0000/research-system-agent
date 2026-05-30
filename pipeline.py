from typing import TypedDict
import re

from langgraph.graph import StateGraph, END

from agents import writer_chain, critic_chain
from tools import web_search, scrape_url


class ResearchState(TypedDict):
    topic: str
    search_results: str
    scraped_content: str
    report: str
    feedback: str


def search_node(state: ResearchState):
    print("\nSTEP 1 - Search node is working...")

    result = web_search.invoke({
        "query": f"Find recent, reliable, and detailed information about: {state['topic']}"
    })

    return {"search_results": result}


def reader_node(state: ResearchState):
    print("\nSTEP 2 - Reader node is scraping content...")

    urls = re.findall(r"URL:\s*(https?://\S+)", state["search_results"])

    if urls:
        scraped = scrape_url.invoke({"url": urls[0]})
    else:
        scraped = "No URL found to scrape."

    return {"scraped_content": scraped}


def writer_node(state: ResearchState):
    print("\nSTEP 3 - Writer node is drafting report...")

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    report = writer_chain.invoke({
        "topic": state["topic"],
        "research": research_combined
    })

    return {"report": report}


def critic_node(state: ResearchState):
    print("\nSTEP 4 - Critic node is reviewing report...")

    feedback = critic_chain.invoke({
        "report": state["report"]
    })

    return {"feedback": feedback}


def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("search", search_node)
    graph.add_node("reader", reader_node)
    graph.add_node("writer", writer_node)
    graph.add_node("critic", critic_node)

    graph.set_entry_point("search")

    graph.add_edge("search", "reader")
    graph.add_edge("reader", "writer")
    graph.add_edge("writer", "critic")
    graph.add_edge("critic", END)

    return graph.compile()


def run_research_pipeline(topic: str):
    app = build_graph()

    final_state = app.invoke({
        "topic": topic,
        "search_results": "",
        "scraped_content": "",
        "report": "",
        "feedback": ""
    })

    print("\nFinal Report:\n")
    print(final_state["report"])

    print("\nCritic Feedback:\n")
    print(final_state["feedback"])

    return final_state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)


# from agents import (
#     build_reader_agent,
#     build_search_agent,
#     writer_chain,
#     critic_chain
# )


# def run_research_pipeline(topic: str) -> dict:

#     state = {}

#     # ==================================================
#     # STEP 1 - SEARCH AGENT
#     # ==================================================

#     print("\n" + "=" * 50)
#     print("STEP 1 - Search Agent is working...")
#     print("=" * 50)

#     search_agent = build_search_agent()

#     search_result = search_agent.invoke({
#         "messages": [
#             (
#                 "user",
#                 f"Find recent, reliable, and detailed information about: {topic}"
#             )
#         ]
#     })

#     # store search results
#     state["search_results"] = search_result["messages"][-1].content

#     print("\nSearch Results:\n")
#     print(state["search_results"])

#     # ==================================================
#     # STEP 2 - READER AGENT
#     # ==================================================

#     print("\n" + "=" * 50)
#     print("STEP 2 - Reader Agent is scraping content...")
#     print("=" * 50)

#     reader_agent = build_reader_agent()

#     reader_result = reader_agent.invoke({
#         "messages": [
#             (
#                 "user",
#                 f"""
# Based on the following search results about '{topic}',

# pick the most relevant URL and scrape it for deeper content.

# Search Results:
# {state['search_results'][:800]}
# """
#             )
#         ]
#     })

#     # store scraped content
#     state["scraped_content"] = reader_result["messages"][-1].content

#     print("\nScraped Content:\n")
#     print(state["scraped_content"])

#     # ==================================================
#     # STEP 3 - WRITER CHAIN
#     # ==================================================

#     print("\n" + "=" * 50)
#     print("STEP 3 - Writer is drafting the report...")
#     print("=" * 50)

#     research_combined = (
#         f"SEARCH RESULTS:\n{state['search_results']}\n\n"
#         f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
#     )

#     state["report"] = writer_chain.invoke({
#         "topic": topic,
#         "research": research_combined
#     })

#     print("\nFinal Report:\n")
#     print(state["report"])

#     # ==================================================
#     # STEP 4 - CRITIC CHAIN
#     # ==================================================

#     print("\n" + "=" * 50)
#     print("STEP 4 - Critic is reviewing the report...")
#     print("=" * 50)

#     state["feedback"] = critic_chain.invoke({
#         "report": state["report"]
#     })

#     print("\nCritic Feedback:\n")
#     print(state["feedback"])

#     return state


# # ==================================================
# # MAIN
# # ==================================================
   

# if __name__ == "__main__":

#     topic = input("\nEnter a research topic: ")

#     run_research_pipeline(topic)
