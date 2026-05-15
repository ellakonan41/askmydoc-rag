# AskMyDoc

## Description

AskMyDoc est une application Streamlit qui permet de poser des questions sur le contenu d’un fichier PDF. Le document est chargé, découpé en vecteurs, puis consulté par un modèle OpenAI pour obtenir des réponses et afficher les sources.

## Fonctionnalités

- Téléversement d’un PDF
- Extraction et découpe du texte
- Indexation en vecteurs avec Chroma
- Recherche de réponses via un modèle OpenAI
- Affichage des sources et pages utilisées

## Installation

1. Créer et activer un environnement virtuel Python :

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Installer les dépendances :

```powershell
pip install -r requirements.txt
```

3. Créer un fichier `.env` à la racine du projet :

```text
OPENAI_API_KEY=ton_api_key_openai
```

4. Vérifier que le fichier `.gitignore` contient au moins :

```text
venv/
.env
```

## Utilisation

Lancer l’application Streamlit :

```powershell
streamlit run app.py
```

Puis :

1. Ouvrir l’URL fournie par Streamlit.
2. Téléverser un fichier PDF.
3. Poser une question dans le champ.
4. Consulter la réponse et les sources.

## Structure du projet

- `app.py` - application Streamlit principale
- `utils/pdf_loader.py` - charge le PDF et extrait le contenu
- `utils/text_splitter.py` - découpe le document en chunks
- `utils/embeddings.py` - initialise le modèle d’embeddings OpenAI
- `utils/vectorstore.py` - crée le vectorstore Chroma
- `utils/qa_chain.py` - construit la chaîne de Q&A

## Remarques

- Ne jamais committer le fichier `.env` sur GitHub.
- Si GitHub bloque le push, vérifie que `.env` n’est pas présent dans l’historique Git et que `.gitignore` est bien configuré.
- Tu peux adapter le modèle OpenAI ou les paramètres de découpe selon tes besoins.


