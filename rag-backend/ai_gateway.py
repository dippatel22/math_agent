# CORE AGENT IMPORTS
from guardrails import input_guardrail, output_guardrail
from kb_response_agent import KBResponseAgent
from model_context_protocol import WebSearchAgent_MCP
from kb_search import kb_similarity_search 

#ROUTING CONFIGURATION

from router_agent import HIGH_CONFIDENCE_THRESHOLD, KB_RESPONSE, WEB_SEARCH 


def process_query_through_gateway(query: str, level: str = "unspecified") -> dict:
    """
    The main wrapper function that acts as the AI Gateway, enforcing 
    Input and Output Guardrails around the core RAG logic.
    """
    
    # INPUT GUARDRAIL CHECK
    print("\n[GATEWAY] 1. Checking Input Guardrails...")
    if not input_guardrail(query):
        return {
            "mode": "REJECTED",
            "message": "Input rejected: Query does not meet the strict Math relevancy policy.",
            "status": "400_BAD_INPUT"
        }

    # CORE RAG LOGIC EXECUTION (Routing)
    print("[GATEWAY] 2. Input approved. Running core RAG routing...")
    
    # Execute the KB Search to get hits and distances
    kb_hits_for_routing = kb_similarity_search(query, k=5)
    
    # routing variables
    mode = WEB_SEARCH # Default mode if KB is not confident
    context_for_llm = []
    confidence = 0.0

    if kb_hits_for_routing:
        top_distance = kb_hits_for_routing[0][1]
        # Calculate confidence
        confidence = 1.0 - top_distance 
        if top_distance < HIGH_CONFIDENCE_THRESHOLD:
            mode = KB_RESPONSE
            context_for_llm = kb_hits_for_routing # Use all relevant hits for KB context
            
    print(f"[GATEWAY] 2. Routed to **{mode}**. Top Similarity Score: {confidence:.4f}")
    
    final_solution = ""
    
    # EXECUTE RESPONSE AGENT 
    if mode == KB_RESPONSE:
        print("[GATEWAY] 3. Executing KB Response Agent...")
        final_solution = KBResponseAgent(query, context_for_llm)
        
    elif mode == WEB_SEARCH:
        print("[GATEWAY] 3. Executing MCP Web Search Agent...")
        final_solution = WebSearchAgent_MCP(query) 

    else:
        final_solution = "Error: Routing failure or unhandled mode."

    # OUTPUT GUARDRAIL CHECK 
    print("[GATEWAY] 4. Checking Output Guardrails...")
    
    guarded_output = output_guardrail(final_solution)
    
    if guarded_output != final_solution:
        return {
            "mode": "BLOCKED",
            "message": guarded_output, 
            "status": "403_FORBIDDEN"
        }
    
    # RETURN FINAL RESPONSE
    return {
        "mode": mode,
        "solution": guarded_output,
        "confidence": confidence,
        "status": "200_OK"
    }


