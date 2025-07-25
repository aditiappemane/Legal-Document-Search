# Indian Legal Document Search System

A web-based system for searching Indian legal documents using four different similarity methods:

- Cosine Similarity
- Euclidean Distance
- Maximal Marginal Relevance (MMR)
- Hybrid Similarity (Cosine + Legal Entity Match)

## Features
- Upload and index legal documents (PDF/Word)
- Query interface with side-by-side comparison of retrieval methods
- Performance metrics dashboard (precision, recall, diversity)

## Tech Stack
- Backend: Python (FastAPI), Gemini API for embeddings
- Frontend: React.js (or Streamlit for rapid prototyping)
- Libraries: scikit-learn, numpy, pandas, spaCy, PyPDF2, python-docx

## Directory Structure
```
backend/
frontend/
data/
  documents/
  embeddings/
analysis/
README.md
```

## Getting Started

Follow these steps to set up and run the Indian Legal Document Search System on your machine.

### 1. Prerequisites
- **Python 3.8+**
- **Node.js 16+ and npm**
- **Git**

### 2. Clone the Repository
```
git clone https://github.com/aditiappemane/Legal-Document-Search.git
cd Legal-Document-Search
```

### 3. Backend Setup
```
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

- Create a `.env` file in the `backend/` directory with your Gemini API key:
  ```
  GEMINI_API_KEY=your_actual_gemini_api_key
  ```

- Start the backend server:
  ```
  uvicorn app:app --reload
  ```
  The backend will run at `http://localhost:8000`

### 4. Frontend Setup
```
cd ../frontend
npm install
```
- Ensure your `frontend/package.json` contains:
  ```json
  "proxy": "http://localhost:8000"
  ```
- Start the React app:
  ```
  npm start
  ```
  The frontend will run at `http://localhost:3000`

### 5. Usage
- Open [http://localhost:3000](http://localhost:3000) in your browser.
- **Upload** your legal documents (PDF/DOCX) using the upload form.
- **Enter queries** and view side-by-side results for all four similarity methods.
- **Evaluate metrics** by selecting relevant files and clicking "Evaluate" to see precision, recall, and diversity.

### 6. Troubleshooting
- **No embeddings created?**
  - Check your `.env` file and Gemini API key.
  - Ensure the backend terminal prints your API key (not `None`).
- **CORS or 404 errors in frontend?**
  - Make sure the backend is running and the proxy is set in `package.json`.
- **Text extraction issues?**
  - Ensure your PDFs are not scanned images (use text-based PDFs or DOCX).
- **Other issues?**
  - Check the backend and frontend terminal output for error messages.

---

For more details, see the Analysis and Report sections below or contact the project maintainer.

## Analysis: Performance Report & Recommendations

### 1. **Evaluation Methodology**
- **Test Queries:**
  - "Income tax deduction for education"
  - "GST rate for textile products"
  - "Property registration process"
  - "Court fee structure"
- **Relevant Documents:**
  - For each query, select relevant documents from the dropdown in the Evaluate Metrics form.
- **Metrics Computed:**
  - **Precision@5:** Fraction of top 5 results that are relevant.
  - **Recall:** Fraction of all relevant documents retrieved in the top 5.
  - **Diversity:** Proportion of unique documents in the top 5 (for MMR, also reflects result variety).

### 2. **How to Evaluate**
- Upload your legal documents (PDF/DOCX) via the UI.
- For each test query, select the relevant files in the Evaluate Metrics form.
- Click "Evaluate" to compute and view precision, recall, and diversity for all four methods.
- Compare the side-by-side results and metrics to determine which method performs best for your dataset and queries.

### 3. **Interpreting Metrics**
- **High Precision@5:** Most of the top 5 results are relevant (good for focused queries).
- **High Recall:** Most or all relevant documents are retrieved (important for comprehensive search).
- **High Diversity:** Results are varied, not redundant (especially important for MMR).
- **Low Scores:** May indicate poor semantic matching, insufficient or noisy data, or that the query is not well-represented in the dataset.

### 4. **Recommendations**
- **For Best Results:**
  - Ensure documents are well-formatted and text is extractable (avoid scanned images).
  - Use clear, specific queries for evaluation.
  - Regularly update and expand your dataset for better coverage.
- **Improving Retrieval:**
  - Fine-tune entity extraction (spaCy NER) for legal-specific terms.
  - Experiment with different weights in the hybrid method.
  - Consider using more advanced embedding models if available.
  - Add more labeled queries and relevant sets for robust evaluation.
- **For Production:**
  - Implement user feedback to refine relevance labels.
  - Monitor metrics over time to track improvements.

### 5. **Sample Results Table**
| Query                          | Method    | Precision@5 | Recall | Diversity |
|--------------------------------|-----------|-------------|--------|-----------|
| Income tax deduction for edu   | Cosine    | 0.4         | 0.5    | 1.0       |
| Income tax deduction for edu   | Euclidean | 0.2         | 0.25   | 0.8       |
| Income tax deduction for edu   | MMR       | 0.6         | 1.0    | 1.0       |
| Income tax deduction for edu   | Hybrid    | 0.4         | 0.5    | 1.0       |

> **Note:** Actual results will vary based on your dataset and queries. Use the dashboard to compare and analyze.

---

