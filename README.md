# Multi-Agent Research System ✨

An AI-powered research system utilizing a network of specialized, collaborating AI agents to automatically perform in-depth web research, analyze sources, and generate comprehensive peer-reviewed reports.

## Overview

This project consists of an interactive **Streamlit frontend** and a **FastAPI backend** that orchestrates a multi-agent LangChain pipeline. The AI agents are powered by **Mistral** and utilize tools like **Tavily** for advanced web searching and **BeautifulSoup** for web scraping.

## Agent Architecture

The research pipeline (`pipeline.py`) flows through four distinct AI agents:

1. **Search Agent**: Receives the research topic and performs targeted web searches using the Tavily API to gather the most relevant sources and snippets.
2. **Reader Agent**: Analyzes the initial search results, selects the most relevant URLs, and scrapes their detailed content to extract factual information while ignoring ads and noise.
3. **Writer Agent**: Synthesizes the extracted factual information into a comprehensive professional report, complete with an executive summary, key findings, and source citations.
4. **Critic Agent**: Reviews the final drafted report, providing constructive feedback, identifying possible hallucinations, and scoring the report based on its accuracy and completeness.

## Tech Stack

- **Backend**: FastAPI, Python 3
- **Frontend**: Streamlit (with ultra-premium UI)
- **AI Framework**: LangChain
- **LLM**: Mistral (via `langchain-mistralai`)
- **Web Search**: Tavily Search API
- **Scraping**: requests & BeautifulSoup4

## Prerequisites

Before running the application, ensure you have API keys for:
- [Tavily](https://tavily.com/)
- [Mistral AI](https://mistral.ai/)

## Setup & Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <your-repo-url>
   cd Multi-agent-research-system
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Install frontend dependencies:
   ```bash
   pip install -r frontend/requirements.txt
   ```
   *(Note: You may also need to install the Mistral integration `pip install langchain-mistralai` if it's missing in your environment)*

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   TAVILY_API_KEY="your_tavily_api_key_here"
   MISTRAL_API_KEY="your_mistral_api_key_here"
   ```

## Running the Application

You will need to run the Backend and Frontend simultaneously in two different terminal windows.

### 1. Start the Backend (FastAPI)
From the root directory, start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The backend will be available at `http://127.0.0.1:8000`.

### 2. Start the Frontend (Streamlit)
Open a new terminal, activate your virtual environment, and run:
```bash
streamlit run frontend/app.py
```
The Streamlit app will automatically open in your browser, where you can enter a topic and watch the agents collaborate in real-time.

## Standalone Pipeline Execution
If you wish to test the multi-agent pipeline via the terminal without the frontend/backend:
```bash
python pipeline.py
```
It will prompt you for a topic and stream the agent logs directly to your console.


