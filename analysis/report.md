# Performance Report: Indian Legal Document Search System

## 1. Introduction
This report analyzes the retrieval performance of four similarity methods (Cosine, Euclidean, MMR, Hybrid) on a test set of Indian legal documents. The goal is to determine which method is most effective for legal document search and provide recommendations for improvement.

## 2. Evaluation Methodology
- **Test Queries:**
  - Income tax deduction for education
  - GST rate for textile products
  - Property registration process
  - Court fee structure
- **Dataset:**
  - Indian Income Tax Act sections
  - GST Act provisions
  - Sample court judgments
  - Property law documents
- **Metrics:**
  - Precision@5: Relevant docs in top 5 results
  - Recall: Coverage of relevant documents
  - Diversity: Result variety (unique docs in top 5)

## 3. Results Summary
| Query                          | Method    | Precision@5 | Recall | Diversity |
|--------------------------------|-----------|-------------|--------|-----------|
| Income tax deduction for edu   | Cosine    | 0.4         | 0.5    | 1.0       |
| Income tax deduction for edu   | Euclidean | 0.2         | 0.25   | 0.8       |
| Income tax deduction for edu   | MMR       | 0.6         | 1.0    | 1.0       |
| Income tax deduction for edu   | Hybrid    | 0.4         | 0.5    | 1.0       |
| ...                            | ...       | ...         | ...    | ...       |

> **Note:** Fill in the table with your actual results for each query and method.

## 4. Findings
- **Cosine Similarity:**
  - Good for semantic matching, but may miss legal-specific context.
- **Euclidean Distance:**
  - Sometimes less effective for high-dimensional embeddings.
- **MMR:**
  - Provides more diverse results, useful for broad queries.
- **Hybrid:**
  - Balances semantic similarity and legal entity matching; often best for legal queries.

## 5. Recommendations
- Use Hybrid or MMR for most legal search scenarios.
- Fine-tune entity extraction (NER) for legal-specific terms to improve Hybrid results.
- Expand and diversify the document dataset for better coverage.
- Regularly evaluate with new queries and update relevance labels.
- Consider user feedback to refine relevance and improve the system iteratively.

## 6. Next Steps
- Integrate more advanced embedding models if available.
- Automate batch evaluation for large test sets.
- Monitor metrics over time to track improvements.

---

*For questions or suggestions, contact the project maintainer.* 