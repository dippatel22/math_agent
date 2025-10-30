from tavily import TavilyClient
from google import genai
from typing import List, Dict
from dotenv import load_dotenv


load_dotenv() 

# Configuration
tavily_client = TavilyClient()
llm_client = genai.Client()
LLM_MODEL = 'gemini-2.5-flash'

# The MCP Extraction

def create_mcp_web_rag_prompt(question: str, search_results: List[Dict]) -> str:
    """
    Constructs an LLM prompt that adheres to Model Context Protocol principles:
    Strictly enforcing grounding, attribution, and refusal of ungrounded answers.
    """
    # System/Role Instruction with MCP Guardrails
    system_instruction = (
        "You are a highly constrained, expert research agent specializing in Math and (JEE/Advanced level). "
        "Your response MUST adhere to the following **Model Context Protocol (MCP) rules**:\n"
        "1. **Attribution:** Cite the [Source X] URL(s) immediately after every factual statement or step you use from the context.\n"
        "2. **Grounding (Zero Hallucination):** You MUST use ONLY the content explicitly provided in the [SEARCH CONTEXT]. Do not use any internal knowledge or external information.\n"
        "3. **Refusal:** If the provided [SEARCH CONTEXT] does not contain sufficient information to generate a complete, step-by-step solution, you must output the exact phrase: 'Insufficient context: I cannot construct a complete, grounded solution based only on the provided web snippets.'\n"
        "4. **Format:** Generate the answer as a simplified, numbered, step-by-step solution. Preserve mathematical notation (like LaTeX) exactly.\n"
    )
    
    # Format Context from Web Search (The Content)
    context_sections = []
    for i, result in enumerate(search_results):
        source_tag = f"[Source {i+1}]"
        context_sections.append(
            f"--- {source_tag} ---\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Content: {result.get('content', 'No content available.')}\n"
        )
    
    context_string = "\n\n".join(context_sections)

    # Combine everything into the final prompt
    final_prompt = (
        f"{system_instruction}\n\n"
        f"============================\n"
        f"[SEARCH CONTEXT]\n"
        f"{context_string}\n"
        f"============================\n\n"
        f"[USER QUESTION]\n"
        f"Provide the step-by-step, grounded solution for: '{question}'"
    )
    
    return final_prompt

# Web Search Agent (Final Version with MCP)

def WebSearchAgent_MCP(
    question: str, 
    max_results: int = 5
) -> str:
    """
    Performs a web search and generates an MCP-compliant answer using an LLM.
    """
    print(f" Web Search Agent (MCP) executing search for: '{question[:50]}...'")

    # Retrieval
    try:
        search_response = tavily_client.search(
            query=question, 
            search_depth="advanced", 
            max_results=max_results
        )
        search_results = search_response.get('results', [])
        
        if not search_results:
            return "Insufficient context: I cannot construct a complete, grounded solution based only on the provided web snippets."

    except Exception as e:
        return f" Tavily Search Error: {e}"

    # Extraction & Synthesis (LLM Step)
    rag_prompt = create_mcp_web_rag_prompt(question, search_results)
    
    print(f" Web Agent synthesizing & grounding answer from {len(search_results)} sources...")
    

    try:
        llm_response = llm_client.models.generate_content(
            model=LLM_MODEL,
            contents=[rag_prompt],
        )
        
        return llm_response.text
    
    except Exception as e:
        return f" LLM Generation Error: {e}"

