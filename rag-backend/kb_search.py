from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Tuple, Dict

# Initialize the embedding model
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2') 
EMBEDDING_DIMENSION = 384 

# Define the VectorDB path and collection name
VECTOR_DB_PATH = "./chromadb_math_jee" 
COLLECTION_NAME = "math_jee_collection" 


def get_chroma_collection(collection_name: str):
    """Initializes the Chroma client and gets the target collection."""
    try:
        chroma_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        
        collection = chroma_client.get_collection(
            name=collection_name, 
            embedding_function=None 
        )
        print(f" Successfully connected to collection: {collection_name}")
        return collection
    except Exception as e:
        print(f" Error connecting to ChromaDB or collection: {e}")
        print("Ensure the collection exists and the path is correct.")
        return None

# KB Search 

def kb_similarity_search(
    question: str, 
    k: int = 5, 
) -> List[Tuple[str, float]]:
    """
    Embeds the user's question and performs a similarity search on the VectorDB.

    Args:
        question: The user's question (e.g., "What is the formula for integration by parts?").
        k: The number of top-k most relevant results to retrieve.

    Returns:
        A list of tuples: [(document_content, distance_score), ...] 
        Sorted by relevance (lowest distance first).
    """
    
    # Get the VectorDB collection
    collection = get_chroma_collection(COLLECTION_NAME)
    if collection is None:
        return []

    # Embed the user's question
    print(f"⚙️ Embedding question: '{question[:30]}...'")
    query_vector = EMBEDDING_MODEL.encode([question]).tolist()
    
    # Perform the similarity search
    try:
        results = collection.query(
            query_embeddings=query_vector,
            n_results=k,
            include=['documents', 'distances']
        )
        
        retrieved_documents = []
        if results and results['documents'] and results['distances']:
            documents = results['documents'][0]
            distances = results['distances'][0]
            
            for doc, dist in zip(documents, distances):
                retrieved_documents.append((doc, dist))
        
        print(f" Retrieved {len(retrieved_documents)} results.")
        return retrieved_documents
        
    except Exception as e:
        print(f" Error during similarity search: {e}")
        return []


