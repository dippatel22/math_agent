import os
from tavily import TavilyClient
from google import genai
from typing import List, Dict
from dotenv import load_dotenv 
load_dotenv()

# Configuration 

from tavily import TavilyClient
tavily_client = TavilyClient()
llm_client = genai.Client()
LLM_MODEL = 'gemini-2.5-flash' 

def create_web_rag_prompt(question: str, search_results: List[Dict]) -> str:
    """
    Constructs a RAG prompt using external web search results as context.
    """
    # System/Role Instruction
    system_instruction = (
        "You are a professional, factual, and helpful research assistant. "
        "Your goal is to answer the user's question accurately using ONLY the "
        "information provided in the [SEARCH RESULTS] section. "
        "If the search results do not contain the answer, you must state: "
        "'I could not find a definitive answer in the search results.' "
        "Answer concisely and use the source URLs for grounding."
    )
    
    # Format Context from Web Search
    context_sections = []
    for i, result in enumerate(search_results):
        context_sections.append(
            f"--- Source {i+1} ---\n"
            f"Title: {result.get('title', 'N/A')}\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Content: {result.get('content', 'No content available.')}\n"
        )
    
    context_string = "\n\n".join(context_sections)

    # Combine everything into the final prompt
    final_prompt = (
        f"{system_instruction}\n\n"
        f"============================\n"
        f"[SEARCH RESULTS]\n"
        f"{context_string}\n"
        f"============================\n\n"
        f"[USER QUESTION]\n"
        f"Based ONLY on the search results, answer the question: '{question}'"
    )
    
    return final_prompt

# Main Web Search Agent Function

def WebSearchAgent(
    question: str, 
    max_results: int = 5
) -> str:
    """
    Performs a web search and generates an answer using an LLM.

    Args:
        question: The user's original question.
        max_results: The number of top search results to retrieve and use as context.

    Returns:
        The final generated answer string.
    """
    print(f"Web Search Agent executing search for: '{question[:50]}...'")

    # Perform the Search using Tavily
    try:
        
        search_response = tavily_client.search(
            query=question, 
            search_depth="advanced", 
            max_results=max_results
        )
        
        search_results = search_response.get('results', [])
        
        if not search_results:
            return "Web Search failed: Could not retrieve any search results."

    except Exception as e:
        return f" Tavily Search Error: Failed to perform web search. Check your TAVILY_API_KEY. Details: {e}"

    # Construct the RAG Prompt
    rag_prompt = create_web_rag_prompt(question, search_results)
    
    print(f" Web Search Agent synthesizing answer from {len(search_results)} sources...")

    # Generate the Final Answer using the LLM
    try:
        llm_response = llm_client.models.generate_content(
            model=LLM_MODEL,
            contents=[rag_prompt],
        )
        
        return llm_response.text
    
    except Exception as e:
        return f" LLM Generation Error: Could not connect to the model. Details: {e}"


