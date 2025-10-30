from google import genai
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()

# Configuration
client = genai.Client()
LLM_MODEL = 'gemini-2.5-flash'


def create_rag_prompt(question: str, retrieved_data: List[Tuple[str, float]]) -> str:
    """
    Constructs the final, structured prompt for the LLM.
    """
    
    # System/Role Instruction
    system_instruction = (
        "You are an expert Math and JEE tutor. Your task is to provide a comprehensive, "
        "simplified, and step-by-step solution to the user's question. "
        "**You MUST ONLY use the information provided in the [CONTEXT] section below.** "
        "If the context does not contain the answer, you must politely state: "
        "'The necessary information for a complete answer is not available in the knowledge base.'\n"
        
        "**CRITICAL OUTPUT FORMATTING RULES:**\n"
        "1. **Structure:** The entire output MUST be structured using **Markdown Headings** (`### Step X: Concept`) for each step.\n"
        "2. **LaTeX:** You MUST use perfect **block LaTeX** for all final equations, formulas, and symbolic results. Use double dollar signs (`$$`) to enclose block equations.\n"
        "3. **Readability:** Use bold text and numbered lists within steps to clearly explain the reasoning.\n"
        "4. **No conversational filler:** Do NOT include introductory phrases like 'Here is the solution' or concluding sentences. Start immediately with '### Step 1:'\n"
        
        "**EXAMPLE REQUIRED FORMAT:**\n"
        "### Step 1: Identify Given Values\n"
        "The problem is based on the **Binomial Theorem** from Document 2. The formula is:\n"
        "$$ (x+y)^n = \\sum_{k=0}^n \\binom{n}{k} x^{n-k} y^k $$\n"
        "### Step 2: Apply Formula\n"
        "..."
    )
    
    # Context Section Construction
    context_text = "\n\n[CONTEXT]\n"
    for i, (doc_content, distance) in enumerate(retrieved_data):
        context_text += f"Document {i+1} (Distance: {distance:.4f}): {doc_content}\n"

    # Final Prompt
    final_prompt = f"{system_instruction}\n\n{context_text}\n\n[USER QUESTION]: {question}"
    
    return final_prompt

# Main KB Response Agent Function
def KBResponseAgent(
    question: str, 
    retrieved_data: List[Tuple[str, float]]
) -> str:
    """
    Generates a final answer using an LLM based on the retrieved KB content.

    Args:
        question: The user's original question.
        retrieved_data: The payload from the VectorDB search.

    Returns:
        The generated final answer string.
    """
    if not retrieved_data:
        return "KB Response Agent failed: No relevant context was provided."

    # Construct the RAG Prompt
    rag_prompt = create_rag_prompt(question, retrieved_data)

    print(" KB Response Agent generating answer...")
    
    try:
        # Call the Gemini API
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=[rag_prompt],
        )
        
        # Return the generated text
        return response.text
    
    except Exception as e:
        return f" LLM Generation Error: Could not connect to the model or process the request. Details: {e}"

