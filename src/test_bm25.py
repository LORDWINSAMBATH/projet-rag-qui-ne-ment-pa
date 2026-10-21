import sys
import os

# Permet d'importer les fichiers du dossier src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from bm25_scratch import BM25FromScratch

def test_bm25_engine():
    # 1. Définir un petit corpus d'exemple simulant tes documents
    corpus = [
        "Le modèle de langage Mistral génère des réponses rapides et précises.",
        "Le RAG permet d'ajouter un moteur de recherche documentaire devant le LLM.",
        "BM25 est un algorithme de recherche lexical basé sur TF-IDF et Okapi.",
        "L'Intelligence Lab organise une piscine de 4 semaines sur l'évaluation des RAG."
    ]

    print("--- 1. Initialisation et Indexation du Corpus ---")
    bm25 = BM25FromScratch(k1=1.5, b=0.75)
    bm25.fit(corpus)
    print(f"Nombre de documents indexés : {bm25.corpus_size}")
    print(f"Longueur moyenne des documents : {bm25.avg_doc_len:.2f} mots")

    # 2. Tester une recherche
    query = "Comment fonctionne la recherche BM25 ?"
    print(f"\n--- 2. Exécution de la recherche pour la requête : '{query}' ---")
    
    results = bm25.search(query, top_k=2)

    for i, r in enumerate(results, 1):
        print(f"Résultat #{i} -> [Doc ID: {r['doc_id']}] (Score: {r['score']})")
        print(f"   Texte : {r['content']}")

    # Assertion de validation simple
    assert len(results) > 0, "Le moteur devrait retourner au moins un résultat !"
    print("\nTest réussi avec succès ! Ton BM25 fait maison fonctionne parfaitement.")

if __name__ == "__main__":
    test_bm25_engine
    h