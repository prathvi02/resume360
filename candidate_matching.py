from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import torch

def encode_text(texts, model_name="distilbert-base-uncased"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.numpy()

def calculate_similarity(job_description_vector, resume_vectors):
    similarities = cosine_similarity(job_description_vector, resume_vectors)
    return similarities.flatten()

def rank_candidates(job_description, resumes, model_name="distilbert-base-uncased"):

    job_vector = encode_text([job_description], model_name)
    resume_vectors = encode_text(resumes, model_name)
    
    scores = calculate_similarity(job_vector, resume_vectors)
    
    ranked_indices = scores.argsort()[::-1]
    return ranked_indices, scores

