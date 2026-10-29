import json
import os
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Chargement d'un modèle d'embedding léger et performant
MODEL_NAME = "all-MiniLM-L6-v2"
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        print(f"[Hybride] Chargement du modèle d'embedding : {MODEL_NAME}...")
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def hybrid_search_fallback(query_text, bm25_results, corpus_chunks, corpus_embeddings=None):
    """
    Fonction de recherche hybride avec stratégie de repli (fallback).
    Si le BM25 ne renvoie rien, on bascule sur une recherche sémantique dense 
    et on retourne les résultats au format compatible (index de page).
    """
    # 1. Si le BM25 a trouvé des résultats, on les utilise
    if bm25_results and len(bm25_results) > 0:
        return bm25_results
    
    # 2. Stratégie de repli (Fallback) : Recherche dense par similarité sémantique
    print(f"[Hybride] BM25 inactif ou vide. Bascule en recherche dense pour : '{query_text}'")
    
    model = get_embedding_model()
    query_embedding = model.encode(query_text, convert_to_tensor=True)
    
    if corpus_embeddings is None and corpus_chunks:
        corpus_embeddings = model.encode(corpus_chunks, convert_to_tensor=True)
    
    if not corpus_chunks or corpus_embeddings is None:
        return []

    # Calcul de la similarité cosinus entre la requête et les chunks du corpus
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    
    # Récupérer les meilleurs indices (top_k=10 pour correspondre à la demande du pipeline)
    top_k = min(10, len(corpus_chunks))
    top_results = np.argsort(cos_scores.cpu().numpy())[::-1][:top_k]
    
    # Format de sortie compatible avec le pipeline (dictionnaire avec 'doc_id' et 'score')
    dense_results = [
        {"doc_id": int(idx), "score": float(cos_scores[idx])} 
        for idx in top_results
    ]
    return dense_results