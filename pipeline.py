import json
from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)

async def run_research_pipeline_stream(topic: str):
    state = {}

    def event(type_, data):
        return json.dumps({"type": type_, "data": data}) + "\n"

    # ===============================
    # STEP 1 - SEARCH AGENT
    # ===============================
    yield event("status", "Initializing Search Agent...")
    
    search_agent = build_search_agent()
    
    yield event("status", f"Searching the web for: {topic}")

    search_result = await search_agent.ainvoke(
        {
            "messages": [
                (
                    "user",
                    f"""
Search the web for recent, reliable and detailed information about:

{topic}

Use the web_search tool.

Return all search results with:
- Title
- URL
- Snippet

Do not summarize.
"""
                )
            ]
        }
    )

    state["search_results"] = search_result["messages"][-1].content
    yield event("status", "Web search completed.")

    # ===============================
    # STEP 2 - READER AGENT
    # ===============================
    yield event("status", "Initializing Reader Agent...")
    
    reader_agent = build_reader_agent()
    
    yield event("status", "Reading and scraping the best source...")

    reader_result = await reader_agent.ainvoke(
        {
            "messages": [
                (
                    "user",
                    f"""
Topic:
{topic}

Search Results:

{state["search_results"][:2000]}

Instructions:

1. Select ONLY the single most reliable and relevant URL.
2. Scrape that URL using the scrape_url tool.
3. Extract only meaningful factual information.
4. Ignore advertisements and navigation text.
5. Remove duplicate information.
6. Produce one concise research summary.
7. Mention if the URL could not be scraped.
"""
                )
            ]
        }
    )

    state["scraped_content"] = reader_result["messages"][-1].content
    yield event("status", "Source reading completed.")

    # ===============================
    # STEP 3 - WRITER
    # ===============================
    yield event("status", "Drafting research report...")

    research = f"""
SEARCH RESULTS

{state["search_results"][:1500]}

SCRAPED CONTENT

{state["scraped_content"][:2000]}
"""

    report_content = ""
    # Stream the writer chain
    async for chunk in writer_chain.astream(
        {
            "topic": topic,
            "research": research,
        }
    ):
        report_content += chunk
        yield event("report_chunk", chunk)

    state["report"] = report_content
    yield event("status", "Report drafting completed. Awaiting critic review...")

    # ===============================
    # STEP 4 - CRITIC
    # ===============================
    yield event("status", "Critic Agent reviewing report...")

    state["feedback"] = await critic_chain.ainvoke(
        {
            "report": state["report"]
        }
    )

    yield event("feedback", state["feedback"])
    yield event("status", "Research complete.")
    yield event("done", True)


if __name__ == "__main__":
    import asyncio
    async def main():
        topic = input("\nEnter a research topic: ")
        async for chunk in run_research_pipeline_stream(topic):
            print(chunk, end="")
            
    asyncio.run(main())