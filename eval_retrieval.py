"""
Évaluation de la recherche (retrieval) d'AskMyDoc.

Question posée : pour chaque question du jeu de test, est-ce que la page
qui contient la réponse fait partie des passages récupérés ?

Métrique : taux de réussite (hit rate) = questions où la bonne page est retrouvée / total.
Les questions "hors document" (page = null) ne sont pas utilisées ici :
elles servent à vérifier à la main que l'application répond "je ne sais pas".

Utilisation :  python eval_retrieval.py
"""

import json
import os
import sys
sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from utils.embeddings import get_embeddings_model

PDF_PATH = "eval/guide_atelier_verdane.pdf"
QUESTIONS_PATH = "eval/questions.json"

# Les configurations à comparer. On ne change qu'un réglage à la fois
# par rapport à la configuration actuelle de l'application (la première).
CONFIGS = [
    {"nom": "Actuelle (500 car., k=3, MMR)", "chunk_size": 500, "overlap": 50, "k": 3, "search_type": "mmr"},
    {"nom": "Similarité simple", "chunk_size": 500, "overlap": 50, "k": 3, "search_type": "similarity"},
    {"nom": "k=5", "chunk_size": 500, "overlap": 50, "k": 5, "search_type": "mmr"},
    {"nom": "Morceaux de 1000 car.", "chunk_size": 1000, "overlap": 100, "k": 3, "search_type": "mmr"},
]


def main():
    load_dotenv(dotenv_path=".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY introuvable dans le fichier .env")

    # 1. Charger le PDF (une page = un document, avec metadata["page"] qui commence à 0)
    docs = PyPDFLoader(PDF_PATH).load()

    # 2. Charger les questions qui ont une page attendue
    with open(QUESTIONS_PATH, encoding="utf-8") as f:
        questions = [q for q in json.load(f) if q["page"] is not None]

    embeddings = get_embeddings_model(api_key)
    resultats = []

    for i, cfg in enumerate(CONFIGS):
        # 3. Découper et indexer avec les réglages de cette configuration.
        #    Un nom de collection différent par config évite de mélanger les index.
        splitter = RecursiveCharacterTextSplitter(chunk_size=cfg["chunk_size"], chunk_overlap=cfg["overlap"])
        chunks = splitter.split_documents(docs)
        vectordb = Chroma.from_documents(chunks, embeddings, collection_name=f"eval_{i}")
        retriever = vectordb.as_retriever(search_type=cfg["search_type"], search_kwargs={"k": cfg["k"]})

        # 4. Pour chaque question : la bonne page est-elle dans les passages récupérés ?
        reussites = 0
        echecs = []
        for q in questions:
            passages = retriever.invoke(q["question"])
            pages_trouvees = {p.metadata["page"] + 1 for p in passages}  # +1 : pages numérotées à partir de 1
            if q["page"] in pages_trouvees:
                reussites += 1
            else:
                echecs.append((q["question"], q["page"], sorted(pages_trouvees)))

        taux = reussites / len(questions)
        resultats.append((cfg["nom"], len(chunks), reussites, len(questions), taux))

        print(f"\n=== {cfg['nom']} : {reussites}/{len(questions)} ({taux:.0%}) — {len(chunks)} morceaux")
        for question, attendue, trouvees in echecs:
            print(f"\n  ✗ {question}  → page attendue {attendue}, pages trouvées {trouvees}")
            for p in retriever.invoke(question):
                extrait = p.page_content.replace("\n", " ")[:150]
                print(f"      - page {p.metadata['page'] + 1} : {extrait}...")

        vectordb.delete_collection()

    # 5. Tableau récapitulatif
    print("\n\nRÉCAPITULATIF")
    print(f"{'Configuration':<32}{'Morceaux':>10}{'Réussite':>12}")
    for nom, n_chunks, ok, total, taux in resultats:
        print(f"{nom:<32}{n_chunks:>10}{f'{ok}/{total} ({taux:.0%})':>12}")


if __name__ == "__main__":
    main()
