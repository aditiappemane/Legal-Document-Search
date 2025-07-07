# Similarity methods for legal document retrieval

import numpy as np

def cosine_similarity(query_emb, doc_emb):
    # Both are 1D numpy arrays
    num = np.dot(query_emb, doc_emb)
    denom = np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
    return num / denom if denom != 0 else 0.0

def euclidean_distance(query_emb, doc_emb):
    return float(np.linalg.norm(query_emb - doc_emb))

def mmr(query_emb, doc_embs, doc_names, lambda_param=0.5, top_n=5):
    # doc_embs: list of numpy arrays, doc_names: list of filenames
    selected = []
    selected_names = []
    candidates = list(range(len(doc_embs)))
    # Precompute cosine similarities
    sim_to_query = [cosine_similarity(query_emb, emb) for emb in doc_embs]
    while len(selected) < top_n and candidates:
        mmr_scores = []
        for idx in candidates:
            if not selected:
                diversity = 0
            else:
                diversity = max([cosine_similarity(doc_embs[idx], doc_embs[s]) for s in selected])
            mmr_score = lambda_param * sim_to_query[idx] - (1 - lambda_param) * diversity
            mmr_scores.append((idx, mmr_score))
        # Select the candidate with the highest MMR score
        best_idx, _ = max(mmr_scores, key=lambda x: x[1])
        selected.append(best_idx)
        selected_names.append(doc_names[best_idx])
        candidates.remove(best_idx)
    # Return list of (filename, similarity) for selected docs
    return [(doc_names[i], sim_to_query[i]) for i in selected]

def hybrid_similarity(query_emb, doc_embs, doc_names, legal_entity_scores):
    # Returns list of (filename, hybrid_score)
    scores = []
    for i, (doc_emb, name) in enumerate(zip(doc_embs, doc_names)):
        cos = cosine_similarity(query_emb, doc_emb)
        hybrid = 0.6 * cos + 0.4 * legal_entity_scores[i]
        scores.append((name, hybrid))
    return sorted(scores, key=lambda x: -x[1])[:5] 