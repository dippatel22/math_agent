import os
from tavily import TavilyClient
from google import genai
from typing import List, Dict
from dotenv import load_dotenv 
load_dotenv()

# Configuration 
tavily_client = TavilyClient()
llm_client = genai.Client()
LLM_MODEL = 'gemini-2.5-flash'

def create_web_rag_prompt(question: str, search_results: List[Dict]) -> str:
    """
    Constructs an LLM prompt with specific instructions for cleaning, 
    parsing, and extracting a step-by-step math solution from web snippets.
    """
    # System/Role Instruction & EXTRACTION/CLEANING Directives
    system_instruction = (
        "You are an expert Math and JEE solver. Your primary task is to extract "
        "and reconstruct a clear, step-by-step solution to the user's complex math question. "
        "You must follow these steps strictly:\n"
        "1. **Isolation & Cleaning:** Disregard all navigation links, ads, boilerplate text, and irrelevant search results. Focus ONLY on text that looks like a solution or factual explanation.\n"
        "2. **Math Parsing:** Preserve all mathematical notation (LaTeX, formulas, symbols) exactly as you find them.\n"
        "3. **Synthesis:** Combine the isolated, relevant pieces of content into ONE cohesive, step-by-step solution.\n"
        "4. **Guardrail:** If you cannot construct a complete solution from the provided [SEARCH RESULTS], state: 'I found several related concepts but cannot synthesize a complete, grounded solution.' "
    )
    
    # Format Context from Web Search 
    context_sections = []
    for i, result in enumerate(search_results):
        context_sections.append(
            f"--- Source {i+1} ---\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Content:\n{result.get('content', 'No content available.')}\n"
        )
    
    context_string = "\n\n".join(context_sections)

    # Combine everything into the final prompt
    final_prompt = (
        f"{system_instruction}\n\n"
        f"============================\n"
        f"[RAW SEARCH RESULTS (Context for Extraction)]\n"
        f"{context_string}\n"
        f"============================\n\n"
        f"[USER QUESTION]\n"
        f"Generate the full, step-by-step solution for: '{question}'"
    )
    
    return final_prompt

# Web Search Agent 

def WebSearchAgent(
    question: str, 
    max_results: int = 7 
) -> str:
    """
    Performs a web search, cleans snippets via LLM instruction, and generates a final answer.
    """
    print(f" Web Search Agent executing advanced search for: '{question[:50]}...'")

   
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

  
    rag_prompt = create_web_rag_prompt(question, search_results)
    
    print(f" Web Agent synthesizing & extracting solution from {len(search_results)} sources...")

    try:
        llm_response = llm_client.models.generate_content(
            model=LLM_MODEL,
            contents=[rag_prompt],
        )
        
        return llm_response.text
    
    except Exception as e:
        return f" LLM Generation Error: Could not connect to the model. Details: {e}"
