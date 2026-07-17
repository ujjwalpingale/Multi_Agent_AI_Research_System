from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# MODEL
# =====================================================

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0
)

# =====================================================
# SEARCH AGENT
# =====================================================

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
You are an expert web research agent.

Your ONLY job is to search the web.

IMPORTANT RULES:

1. ALWAYS use the web_search tool.
2. NEVER answer using your own knowledge.
3. NEVER summarize the search results.
4. NEVER rewrite the search results.
5. NEVER remove URLs.
6. NEVER change Titles.
7. NEVER change Snippets.
8. Return ALL search results exactly as returned by the tool.
9. Preserve every Title, URL and Snippet.
10. Your final answer should ONLY contain the raw search results.

Do not explain anything.
Do not add introductions.
Do not add conclusions.
Do not add your own opinions.
"""
    )

# =====================================================
# READER AGENT
# =====================================================

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
You are an expert research analyst.

Your ONLY responsibility is reading webpages.

Instructions:

1. Choose the most relevant URLs.
2. Scrape multiple pages whenever possible.
3. Ignore advertisements, navigation bars and unrelated content.
4. Extract only factual information.
5. Remove duplicate information.
6. Combine information into one detailed research summary.
7. Mention if a page could not be scraped.
8. Do NOT invent facts.
"""
    )

# =====================================================
# WRITER
# =====================================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a professional research writer.

Rules:

- Use ONLY the provided research.
- Never invent facts.
- Never guess information.
- Mention if information is missing.
- Combine multiple sources.
- Avoid repetition.
- Use professional language.
- Produce a detailed report.
"""
    ),
    (
        "human",
        """
Topic:
{topic}

Research:
{research}

Write a professional report with:

1. Executive Summary

2. Introduction

3. Key Findings
   - Minimum 4 detailed findings.

4. Detailed Analysis

5. Conclusion

6. Sources
   - List EVERY source URL found in the research.
"""
    )
])

writer_chain = writer_prompt | llm | StrOutputParser()

# =====================================================
# CRITIC
# =====================================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a senior research reviewer.

Evaluate the report objectively.

Check:

- Accuracy
- Completeness
- Clarity
- Structure
- Quality of evidence
- Possible hallucinations
- Missing information

Be constructive.
"""
    ),
    (
        "human",
        """
Report:

{report}

Respond EXACTLY in this format.

Score: X/10

Strengths:
- ...
- ...

Weaknesses:
- ...
- ...

Possible Hallucinations:
- ...

Suggestions:
- ...

Final Verdict:
...
"""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()