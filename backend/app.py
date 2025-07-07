from dotenv import load_dotenv
load_dotenv()
import os
print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))
from fastapi import FastAPI, UploadFile, File, Body
from PyPDF2 import PdfReader
from docx import Document
import numpy as np
from gemini_client import get_gemini_embedding
from similarity import cosine_similarity, euclidean_distance
from entity_match import legal_entity_match
from similarity import hybrid_similarity
from typing import List

app = FastAPI()

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/documents')
os.makedirs(DATA_DIR, exist_ok=True)

EMBEDDINGS_DIR = os.path.join(os.path.dirname(__file__), '../data/embeddings')
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

@app.get("/")
def read_root():
    return {"message": "Indian Legal Document Search System Backend"}

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    # Extract text
    if filename.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif filename.lower().endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file type. Only PDF and DOCX are supported."}
    # Save extracted text
    text_path = file_path + ".txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)
    # Generate and save embedding
    try:
        embedding = get_gemini_embedding(text)
        emb_path = os.path.join(EMBEDDINGS_DIR, filename + ".npy")
        np.save(emb_path, np.array(embedding))
        emb_shape = np.array(embedding).shape
    except Exception as e:
        return {"filename": filename, "text": text[:1000], "embedding_error": str(e)}
    return {"filename": filename, "text": text[:1000], "embedding_shape": emb_shape}

@app.post("/search/")
async def search_documents(query: str = Body(..., embed=True)):
    try:
        query_embedding = get_gemini_embedding(query)
        query_emb = np.array(query_embedding)
    except Exception as e:
        return {"query": query, "embedding_error": str(e)}
    # Load all document embeddings and texts
    results = []
    doc_names = []
    doc_embs = []
    doc_texts = []
    for fname in os.listdir(EMBEDDINGS_DIR):
        if fname.endswith('.npy'):
            doc_emb = np.load(os.path.join(EMBEDDINGS_DIR, fname))
            results.append((fname, doc_emb))
            doc_names.append(fname)
            doc_embs.append(doc_emb)
            # Load corresponding text
            base = fname[:-4]  # remove .npy
            txt_path = os.path.join(DATA_DIR, base)
            if os.path.exists(txt_path + '.pdf.txt'):
                with open(txt_path + '.pdf.txt', encoding='utf-8') as f:
                    doc_texts.append(f.read())
            elif os.path.exists(txt_path + '.docx.txt'):
                with open(txt_path + '.docx.txt', encoding='utf-8') as f:
                    doc_texts.append(f.read())
            else:
                doc_texts.append("")
    # Compute similarities
    cosine_scores = []
    euclidean_scores = []
    for fname, doc_emb in results:
        cos = cosine_similarity(query_emb, doc_emb)
        cosine_scores.append((fname, float(cos)))
        euc = euclidean_distance(query_emb, doc_emb)
        euclidean_scores.append((fname, float(euc)))
    # Sort and get top 5
    cosine_top5 = sorted(cosine_scores, key=lambda x: -x[1])[:5]
    euclidean_top5 = sorted(euclidean_scores, key=lambda x: x[1])[:5]
    # MMR top 5
    from similarity import mmr
    mmr_top5 = mmr(query_emb, doc_embs, doc_names, lambda_param=0.5, top_n=5)
    # Hybrid similarity
    legal_entity_scores = legal_entity_match(query, doc_texts)
    hybrid_top5 = hybrid_similarity(query_emb, doc_embs, doc_names, legal_entity_scores)
    return {
        "query": query,
        "cosine_top5": cosine_top5,
        "euclidean_top5": euclidean_top5,
        "mmr_top5": mmr_top5,
        "hybrid_top5": hybrid_top5
    }

def compute_precision_recall(top5, relevant):
    top5_set = set([fname for fname, _ in top5])
    relevant_set = set(relevant)
    precision = len(top5_set & relevant_set) / 5
    recall = len(top5_set & relevant_set) / len(relevant_set) if relevant_set else 0
    return precision, recall

def compute_diversity(top5):
    # Diversity: number of unique documents/entities in top 5 (simple version)
    return len(set([fname for fname, _ in top5])) / 5

@app.post("/evaluate/")
async def evaluate(
    query: str = Body(...),
    relevant: List[str] = Body(...)
):
    # Run search as in /search/
    try:
        query_embedding = get_gemini_embedding(query)
        query_emb = np.array(query_embedding)
    except Exception as e:
        return {"query": query, "embedding_error": str(e)}
    # Load all document embeddings and texts
    results = []
    doc_names = []
    doc_embs = []
    doc_texts = []
    for fname in os.listdir(EMBEDDINGS_DIR):
        if fname.endswith('.npy'):
            doc_emb = np.load(os.path.join(EMBEDDINGS_DIR, fname))
            results.append((fname, doc_emb))
            doc_names.append(fname)
            doc_embs.append(doc_emb)
            # Load corresponding text
            base = fname[:-4]
            txt_path = os.path.join(DATA_DIR, base)
            if os.path.exists(txt_path + '.pdf.txt'):
                with open(txt_path + '.pdf.txt', encoding='utf-8') as f:
                    doc_texts.append(f.read())
            elif os.path.exists(txt_path + '.docx.txt'):
                with open(txt_path + '.docx.txt', encoding='utf-8') as f:
                    doc_texts.append(f.read())
            else:
                doc_texts.append("")
    # Compute similarities
    cosine_scores = [(fname, float(cosine_similarity(query_emb, doc_emb))) for fname, doc_emb in results]
    euclidean_scores = [(fname, float(euclidean_distance(query_emb, doc_emb))) for fname, doc_emb in results]
    cosine_top5 = sorted(cosine_scores, key=lambda x: -x[1])[:5]
    euclidean_top5 = sorted(euclidean_scores, key=lambda x: x[1])[:5]
    from similarity import mmr, hybrid_similarity
    mmr_top5 = mmr(query_emb, doc_embs, doc_names, lambda_param=0.5, top_n=5)
    legal_entity_scores = legal_entity_match(query, doc_texts)
    hybrid_top5 = hybrid_similarity(query_emb, doc_embs, doc_names, legal_entity_scores)
    # Compute metrics
    metrics = {}
    metrics['cosine'] = {}
    metrics['euclidean'] = {}
    metrics['mmr'] = {}
    metrics['hybrid'] = {}
    metrics['cosine']['precision'], metrics['cosine']['recall'] = compute_precision_recall(cosine_top5, relevant)
    metrics['euclidean']['precision'], metrics['euclidean']['recall'] = compute_precision_recall(euclidean_top5, relevant)
    metrics['mmr']['precision'], metrics['mmr']['recall'] = compute_precision_recall(mmr_top5, relevant)
    metrics['hybrid']['precision'], metrics['hybrid']['recall'] = compute_precision_recall(hybrid_top5, relevant)
    metrics['mmr']['diversity'] = compute_diversity(mmr_top5)
    metrics['cosine']['diversity'] = compute_diversity(cosine_top5)
    metrics['euclidean']['diversity'] = compute_diversity(euclidean_top5)
    metrics['hybrid']['diversity'] = compute_diversity(hybrid_top5)
    return {"query": query, "metrics": metrics}

@app.get("/filenames/")
def list_filenames():
    # Return all document embedding filenames (without .npy extension)
    files = [fname[:-4] for fname in os.listdir(EMBEDDINGS_DIR) if fname.endswith('.npy')]
    return {"filenames": files} 