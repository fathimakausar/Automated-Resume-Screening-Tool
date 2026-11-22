"""Similarity features: TF-IDF (default) or sentence-transformer embeddings (optional)."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import config
from cleaner import clean_text

_model = None


def tfidf_similarity(job_text, resume_texts):
    docs = [clean_text(job_text)] + [clean_text(t) for t in resume_texts]
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    matrix = vec.fit_transform(docs)
    return cosine_similarity(matrix[0:1], matrix[1:]).flatten().tolist()


def embedding_similarity(job_text, resume_texts):
    global _model
    from sentence_transformers import SentenceTransformer   # pip install sentence-transformers
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    vecs = _model.encode([job_text] + list(resume_texts), normalize_embeddings=True)
    return (vecs[1:] @ vecs[0]).tolist()


def similarity(job_text, resume_texts):
    """Return (similarities, cap). Falls back to TF-IDF if embeddings are unavailable."""
    if config.SIMILARITY_BACKEND == "embeddings":
        try:
            return embedding_similarity(job_text, resume_texts), config.EMBEDDING_SIMILARITY_CAP
        except Exception as err:
            print(f"[WARN] Embeddings unavailable ({err}); using TF-IDF instead")
    return tfidf_similarity(job_text, resume_texts), config.SIMILARITY_CAP
