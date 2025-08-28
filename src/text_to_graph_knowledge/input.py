"""Simple I/O and preprocessing utilities for converting raw text to structured pieces.

This module provides a small OOP wrapper around textual input sources and simple
preprocessing steps commonly used in downstream pipelines.
"""
from typing import List, Iterable, Optional
import re


class TextInput:
    """Container for one or more documents with preprocessing helpers.

    Attributes
    ----------
    docs : List[str]
        Raw documents stored as strings.
    """

    def __init__(self, docs: Optional[Iterable[str]] = None) -> None:
        self.docs: List[str] = list(docs) if docs is not None else []

    @classmethod
    def from_file(cls, path: str, encoding: str = "utf-8") -> "TextInput":
        with open(path, "r", encoding=encoding) as f:
            text = f.read()
        return cls([text])

    @classmethod
    def from_string(cls, text: str) -> "TextInput":
        return cls([text])

    def add(self, text: str) -> None:
        self.docs.append(text)

    def get_doc(self, idx: int = 0) -> str:
        return self.docs[idx]

    def split_sentences(self, idx: int = 0) -> List[str]:
        """Very small sentence splitter using punctuation heuristics."""
        text = self.get_doc(idx)
        # naive; for production use a proper sentence tokenizer
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s for s in sentences if s]

    def tokenize(self, sentence: str) -> List[str]:
        """Whitespace + punctuation tokenizer; returns lowercase tokens."""
        tokens = re.findall(r"\w+", sentence)
        return [t.lower() for t in tokens]

    def preprocess(self, lower: bool = True, remove_extra_ws: bool = True) -> None:
        new_docs: List[str] = []
        for d in self.docs:
            if remove_extra_ws:
                d = re.sub(r"\s+", " ", d).strip()
            if lower:
                d = d.lower()
            new_docs.append(d)
        self.docs = new_docs
