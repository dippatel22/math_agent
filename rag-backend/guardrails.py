def input_guardrail(user_input: str) -> bool:
    """
    Checks if the user input is strictly related to Math, JEE, or core Science concepts.
    Rejects the input if no relevant keywords are found.
    """
    
    # Define list of allowed keywords
    math_keywords = [
 "math", "mathematics", "algebra", "geometry", "calculus", 
"trigonometry", "probability", "statistics", "integral", "derivative", 
"equation", "formula", "function", "sum", "solve", "proof", 
"differential", "limit", "series", "logarithm", "matrix", "vector", 
"quadratic", "set", "relation", "permutation", "combination", "sequence", 
"progression", "definite", "indefinite", "area", "volume", "complex", 
"number", "domain", "range", "inverse", "linear", "polynomial", 
"rational", "exponent", "continuity", "maxima", "minima", "tangent", 
"normal", "locus", "partial", "system", "scalar", "modulus", 
"argument", "identity", "inequality", "ellipse", "parabola", 
"hyperbola", "circle", "coordinate", "jacobian", "fourier", 
"laplace", "sinc", "cosh", "sinh", "calculate", "find", "prove", 
"explain", "concept", "theorem", "principle", "law", "graph", 
"diagram","approximately","calculate"
    ]
    
    # Check if ANY of the allowed keywords are present in the input
    if any(word in user_input.lower() for word in math_keywords):
        return True
    else:
        # If no math keyword is found, reject the input.
        print("Input Rejected: Query is not recognized as Math related.")
        return False


def output_guardrail(answer: str) -> str:
    """
    Current basic output guardrail (retaining original logic for safety checks).
    """
    if "http" in answer or "malicious" in answer:
        return " Output blocked for safety reasons."
    return answer
