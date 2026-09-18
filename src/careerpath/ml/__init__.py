"""Machine learning, preprocessing, feature engineering, and artifact management package."""

from careerpath.ml.preprocessing import StudentProfilePreprocessor
from careerpath.ml.splitting import DatasetSplitter
from careerpath.ml.features import FeatureExtractor
from careerpath.ml.artifacts import ArtifactManager

__all__ = [
    "StudentProfilePreprocessor",
    "DatasetSplitter",
    "FeatureExtractor",
    "ArtifactManager",
]
