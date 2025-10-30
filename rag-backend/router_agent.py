from typing import List, Tuple, Dict

KB_RESPONSE = "KB_RESPONSE"
WEB_SEARCH = "WEB_SEARCH"

HIGH_CONFIDENCE_THRESHOLD = 0.45


def RouterAgent(
    question: str, 
    kb_search_function: callable, 
    k: int = 1
) -> str:
    """
    Routes the user's question based on the confidence of the top KB search result.

    Args:
        question: The user's original question (e.g., "What is the formula for integration by parts?").
        kb_search_function: The function that performs the KB similarity search 
                            (your 'kb_similarity_search' function).
        k: The number of results to retrieve (we only check the top one, so k=1 is sufficient).

    Returns:
        A string indicating the selected route: 'KB_RESPONSE' or 'WEB_SEARCH'.
    """
    print(f"🕵️ Router Agent analyzing question: '{question[:50]}...'")

    # Perform KB Search
 
    search_results: List[Tuple[str, float]] = kb_search_function(question, k=k)
    
    # Check Confidence of the Top Result
    if search_results:
        top_document, top_distance = search_results[0]
        
        print(f"   - Top result distance: {top_distance:.4f} (Threshold: {HIGH_CONFIDENCE_THRESHOLD})")
        
        if top_distance < HIGH_CONFIDENCE_THRESHOLD:
            print(f"   - Decision: Distance is LOW. Routing to **{KB_RESPONSE}**.")
            return KB_RESPONSE
        else:
            print(f"   - Decision: Distance is HIGH. Routing to **{WEB_SEARCH}**.")
            return WEB_SEARCH
    
    else:
        print(f"   - Decision: No KB results found. Routing to **{WEB_SEARCH}**.")
        return WEB_SEARCH
