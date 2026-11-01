import os
from pathlib import Path
import pymupdf
from collections import Counter

def analyze_corpus_types(pdf_dir="corpus/pdf"):
    pdf_path = Path(pdf_dir)
    if not pdf_path.exists():
        print(f"❌ Le dossier {pdf_dir} est introuvable. Vérifie le chemin.")
        return

    types_count = Counter()
    total_docs = 0

    print(f"🔍 Analyse détaillée des documents dans '{pdf_dir}'...\n")
    print("--- 📄 DÉTAIL PAR DOCUMENT ---")

    for pdf_file in sorted(pdf_path.glob("*.pdf")):
        total_docs += 1
        doc_id = pdf_file.stem
        doc_type = "Autre / Non classé"
        
        # 1. Analyse basée sur les préfixes du nom de fichier
        if "insee" in doc_id.lower():
            doc_type = "Publication INSEE (Conjoncture / Flash)"
        
        # 2. Analyse du contenu de la première page pour affiner la nature
        try:
            with pymupdf.open(pdf_file) as doc:
                if len(doc) > 0:
                    first_page_text = doc[0].get_text("text").lower()
                    
                    if "rapport" in first_page_text or "commission" in first_page_text:
                        doc_type = "Rapport Institutionnel / Commission"
                    elif "bilan" in first_page_text or "financier" in first_page_text or "budget" in first_page_text:
                        doc_type = "Document Budgétaire / Financier"
                    elif "synthese" in first_page_text or "synthèse" in first_page_text:
                        doc_type = "Note de Synthèse"
                    elif "statistique" in first_page_text or "résultats" in first_page_text:
                        doc_type = "Étude / Recueil Statistique"
        except Exception as e:
            print(f"Erreur de lecture sur {doc_id}: {e}")

        types_count[doc_type] += 1
        print(f"• {doc_id} ➔ {doc_type}")

    # Affichage du résumé global
    print("\n" + "=" * 60)
    print(f"📊 RÉSUMÉ GLOBAL DU CORPUS (Total : {total_docs} documents)")
    print("=" * 60)
    for dtype, count in types_count.most_common():
        print(f"• {count} document(s) de type : {dtype}")
    print("=" * 60)

if __name__ == "__main__":
    analyze_corpus_types()