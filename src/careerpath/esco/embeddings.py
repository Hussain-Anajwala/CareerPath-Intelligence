"""Local Sentence Transformers embeddings & FAISS vector search index for ESCO skills and occupations."""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from careerpath.config.logging import logger
from careerpath.config.settings import settings
from careerpath.esco.taxonomy import ESCOTaxonomy, ESCOSkill, ESCOOccupation


class ESCOVectorIndex:
    """Manages local CPU FAISS vector search index for ESCO skills and occupations."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        taxonomy: Optional[ESCOTaxonomy] = None,
    ):
        self.model_name = model_name
        self.model_license = "Apache-2.0 (SentenceTransformers / HuggingFace)"
        self.taxonomy = taxonomy or ESCOTaxonomy()

        logger.info(f"Loading local SentenceTransformer model: {self.model_name}")
        self.encoder = SentenceTransformer(self.model_name)
        self.embedding_dim = self.encoder.get_sentence_embedding_dimension()

        # FAISS Index using Inner Product (Cosine similarity when vectors are L2 normalized)
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.skill_uris: List[str] = []
        self.skill_labels: List[str] = []
        self.is_built: bool = False

    def build_skill_index(self):
        """Encodes all ESCO skills and populates the FAISS index."""
        skills_list = list(self.taxonomy.skills.values())
        if not skills_list:
            logger.warning("No ESCO skills available to index.")
            return

        texts = [f"{sk.preferred_label}: {sk.description}" for sk in skills_list]
        embeddings = self.encoder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

        self.index.reset()
        self.index.add(embeddings.astype(np.float32))

        self.skill_uris = [sk.uri for sk in skills_list]
        self.skill_labels = [sk.preferred_label for sk in skills_list]
        self.is_built = True

        logger.info(f"Successfully built FAISS skill index with {len(skills_list)} vectors (dim={self.embedding_dim}).")

    def search_skills(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Searches ESCO skills for a query text using FAISS cosine similarity."""
        if not self.is_built:
            self.build_skill_index()

        query_emb = self.encoder.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
        scores, indices = self.index.search(query_emb, top_k)

        results = []
        for rank, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.skill_uris):
                continue
            uri = self.skill_uris[idx]
            skill = self.taxonomy.get_skill_by_uri(uri)
            results.append(
                {
                    "rank": rank + 1,
                    "skill_uri": uri,
                    "skill_label": self.skill_labels[idx],
                    "similarity_score": round(float(scores[0][rank]), 4),
                    "skill_type": skill.skill_type if skill else "skill",
                    "description": skill.description if skill else "",
                }
            )
        return results

    def save_index(self, target_dir: Optional[Path] = None):
        """Persists FAISS index and metadata mapping to disk."""
        target_dir = target_dir or (settings.PROCESSED_DATA_DIR / "esco")
        target_dir.mkdir(parents=True, exist_ok=True)

        index_file = target_dir / "esco_skills.faiss"
        meta_file = target_dir / "esco_metadata.json"

        faiss.write_index(self.index, str(index_file))

        metadata = {
            "model_name": self.model_name,
            "embedding_dim": self.embedding_dim,
            "skill_uris": self.skill_uris,
            "skill_labels": self.skill_labels,
            "model_license": self.model_license,
            "num_vectors": len(self.skill_uris),
        }

        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Persisted ESCO FAISS index to {index_file} and metadata to {meta_file}")

    def load_index(self, target_dir: Optional[Path] = None):
        """Loads persisted FAISS index and metadata mapping from disk."""
        target_dir = target_dir or (settings.PROCESSED_DATA_DIR / "esco")
        index_file = target_dir / "esco_skills.faiss"
        meta_file = target_dir / "esco_metadata.json"

        if not index_file.exists() or not meta_file.exists():
            raise FileNotFoundError(f"FAISS index files not found in {target_dir}")

        self.index = faiss.read_index(str(index_file))
        with open(meta_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        self.skill_uris = metadata["skill_uris"]
        self.skill_labels = metadata["skill_labels"]
        self.is_built = True
        logger.info(f"Loaded ESCO FAISS index from {index_file} ({len(self.skill_uris)} vectors).")
