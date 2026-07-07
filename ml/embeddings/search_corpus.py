"""
Top-k similarity search over the scam script corpus FAISS index built by
embed_corpus.py (Sumanth task sheet, section 5: new scam pattern -> embed ->
search top-5 similar -> suggest to analyst).

Run:
    cd ml/embeddings
    python search_corpus.py "Your parcel has been seized by customs, pay fine now"
    python search_corpus.py --k 3 "आपके खाते का केवाईसी ब्लॉक हो जाएगा"
"""
import argparse
import json
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(__file__)
INDEX_PATH = os.path.join(BASE_DIR, "scam_corpus.faiss")
META_PATH = os.path.join(BASE_DIR, "scam_corpus_meta.json")


def load_index() -> tuple[faiss.Index, dict]:
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, encoding="utf-8") as f:
        meta = json.load(f)
    return index, meta


def search(query: str, k: int = 5) -> list[dict]:
    index, meta = load_index()
    model = SentenceTransformer(meta["embed_model"])
    embedding = model.encode([query], normalize_embeddings=True).astype(np.float32)
    scores, positions = index.search(embedding, k)
    results = []
    for score, pos in zip(scores[0], positions[0]):
        if pos < 0:
            continue
        row = meta["rows"][pos]
        results.append({**row, "similarity": float(score)})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="new scam pattern / transcript text")
    parser.add_argument("--k", type=int, default=5, help="number of matches (default 5)")
    args = parser.parse_args()

    for i, r in enumerate(search(args.query, args.k), 1):
        print(f"{i}. [{r['similarity']:.3f}] ({r['language']}/{r['scam_type']}) {r['title']}")
        print(f"   {r['content'][:120]}...")


if __name__ == "__main__":
    main()
