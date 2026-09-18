"""Artifact serialization, metadata management, and integrity tracking."""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import joblib


from careerpath.config.logging import logger
from careerpath.config.settings import settings


class ArtifactManager:
    """Manages saving and loading of fitted ML preprocessors and pipeline artifacts safely."""

    @staticmethod
    def calculate_checksum(file_path: Path) -> str:
        """Calculates SHA-256 hash of an artifact file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @classmethod
    def save_artifact(
        cls,
        artifact: Any,
        artifact_name: str,
        version: str = "v1.0",
        metadata: Optional[Dict[str, Any]] = None,
        target_dir: Optional[Path] = None,
    ) -> Path:
        """Saves a fitted preprocessor/artifact along with metadata and SHA-256 checksum."""
        target_dir = target_dir or (settings.MODELS_DIR / artifact_name / version)
        target_dir.mkdir(parents=True, exist_ok=True)

        artifact_file = target_dir / f"{artifact_name}.joblib"
        joblib.dump(artifact, artifact_file)

        checksum = cls.calculate_checksum(artifact_file)

        metadata_dict = {
            "artifact_name": artifact_name,
            "version": version,
            "file_name": artifact_file.name,
            "sha256_checksum": checksum,
            "user_metadata": metadata or {},
        }

        metadata_file = target_dir / "metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata_dict, f, indent=2)

        logger.info(
            f"Artifact '{artifact_name}' (version {version}) saved to {artifact_file} (SHA256: {checksum[:8]}...)"
        )
        return artifact_file

    @classmethod
    def load_artifact(cls, artifact_file: Path) -> Tuple[Any, Dict[str, Any]]:
        """Loads a saved pipeline artifact and verifies its SHA-256 checksum if metadata exists."""
        if not artifact_file.exists():
            raise FileNotFoundError(f"Artifact file not found at: {artifact_file}")

        metadata_file = artifact_file.parent / "metadata.json"
        metadata = {}

        if metadata_file.exists():
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            expected_checksum = metadata.get("sha256_checksum")
            if expected_checksum:
                actual_checksum = cls.calculate_checksum(artifact_file)
                if actual_checksum != expected_checksum:
                    raise ValueError(
                        f"Checksum mismatch for artifact {artifact_file}. Expected {expected_checksum}, got {actual_checksum}."
                    )

        artifact = joblib.load(artifact_file)
        logger.info(f"Loaded artifact from {artifact_file}")
        return artifact, metadata
