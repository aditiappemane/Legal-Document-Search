# Legal entity matching using NER (e.g., spaCy)

import spacy
nlp = spacy.load("en_core_web_sm")

def extract_legal_entities(text):
    doc = nlp(text)
    # For demo, use ORG, LAW, GPE, PERSON, etc. (customize for legal domain)
    return set([ent.text.lower() for ent in doc.ents if ent.label_ in {"ORG", "LAW", "GPE", "PERSON"}])

def legal_entity_match(query_text, doc_texts):
    query_ents = extract_legal_entities(query_text)
    scores = []
    for doc_text in doc_texts:
        doc_ents = extract_legal_entities(doc_text)
        if not query_ents or not doc_ents:
            scores.append(0.0)
        else:
            overlap = len(query_ents & doc_ents) / len(query_ents | doc_ents)
            scores.append(overlap)
    return scores 