import os
import json
from google import genai
from typing import List, Dict, Tuple
from dotenv import load_dotenv

load_dotenv() 
try:
    client = genai.Client()
except Exception:
    print("WARNING: Gemini client initialization failed. Check GEMINI_API_KEY.")
    
# CONFIGURATION

REFINED_EXAMPLES_FILE = "optimized_examples.json"

# STORAGE AND RETRIEVAL

def load_refined_examples() -> List[Dict]:
    """Loads the persistent store of human-validated examples."""
    if os.path.exists(REFINED_EXAMPLES_FILE):
        with open(REFINED_EXAMPLES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_refined_examples(examples: List[Dict]):
    """Saves the current list of refined examples."""
    with open(REFINED_EXAMPLES_FILE, 'w') as f:
        json.dump(examples, f, indent=4)

# THE REFINEMENT LOGIC

def run_refinement_agent(feedback_item: Dict):
    """
    Analyzes a single piece of human feedback and converts it into a high-quality 
    "Few-Shot Example" to be used in future prompts.
    This process is triggered ONLY for good corrections.
    """
    if feedback_item.get('assessment') not in ['INCORRECT', 'COMPLEX']:
        return 

    query = feedback_item['query']
    correction = feedback_item['correction_text']
    
    refinement_prompt = f"""
    You are a prompt engineer for an AI Math Tutor. Your job is to extract the 
    core knowledge from a human correction to create a reusable, high-quality 
    "Few-Shot Example" for future LLM responses.

    Create a single JSON object with two keys: "question" and "ideal_answer".
    
    --- INPUT ---
    Original Query: {query}
    Human Correction (Gold Standard): {correction}
    
    --- INSTRUCTIONS ---
    1. The "question" must be the core math problem from the query.
    2. The "ideal_answer" must be the clean, simplified, step-by-step solution provided 
       in the Human Correction, formatted with numbered steps and proper LaTeX.
    
    --- REQUIRED JSON OUTPUT ---
    {{
        "question": "[Extracted core question]",
        "ideal_answer": "[Cleaned, step-by-step solution]"
    }}
    """
    
    print(" Refinement Agent: Analyzing human correction...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[refinement_prompt]
        )
        
        refined_example = json.loads(response.text.strip())
        
        examples = load_refined_examples()
        examples.append(refined_example)
        save_refined_examples(examples)
        
        print(f" Refinement successful. Added new example for query: {query[:30]}...")
        
    except json.JSONDecodeError:
        print(" Refinement Agent failed to parse LLM output into JSON.")
    except Exception as e:
        print(f" Refinement Agent failed: {e}")

