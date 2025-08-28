"""Entity linking class that maps detected entity mentions to entries in a KB.

This module includes a simple in-memory KB and fuzzy string matching linking.
"""
from typing import Dict, Iterable, Tuple, Optional
import difflib


class EntityLinker:
    """Link entity mentions to knowledge-base entries.

    The in-memory KB is a mapping of canonical name -> metadata dictionary. The
    `link` method returns the KB key and a score (0..1) or None when no good
    candidate exists.
    """

    def __init__(self, kb: Optional[Dict[str, Dict]] = None):
        self.kb = kb or {}

    def add_entry(self, name: str, metadata: Dict) -> None:
        self.kb[name] = metadata

    def link(self, mention: str, top_n: int = 3, threshold: float = 0.6) -> Optional[Tuple[str, float]]:
        """Return best KB key and similarity score, or None if below threshold."""
        if not self.kb:
            return None
        names = list(self.kb.keys())
        # use difflib's SequenceMatcher via get_close_matches
        matches = difflib.get_close_matches(mention, names, n=top_n, cutoff=threshold)
        if not matches:
            # still compute best ratio to provide a best-effort candidate
            best = max(names, key=lambda n: difflib.SequenceMatcher(None, mention, n).ratio())
            score = difflib.SequenceMatcher(None, mention, best).ratio()
            return (best, score) if score >= threshold else None
        best = matches[0]
        score = difflib.SequenceMatcher(None, mention, best).ratio()
        return (best, score)

    def bulk_link(self, mentions: Iterable[str], **kwargs):
        return {m: self.link(m, **kwargs) for m in mentions}
