from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv  
load_dotenv()  # Load API key before creating client

model = SentenceTransformer('all-MiniLM-L6-v2')

def relevance_score(answer, reference):
    emb1 = model.encode(answer, convert_to_tensor=True)
    emb2 = model.encode(reference, convert_to_tensor=True)
    score = float(util.cos_sim(emb1, emb2).item())
    return score
