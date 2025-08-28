"""Relationship extraction orchestrator combining rule-based and placeholder ML models.

This module defines a high-level class that accepts entity spans and sentences and
returns candidate relationships. It is intentionally modular so you can swap in
more advanced extractors.
"""
from typing import List, Tuple, Iterable, Optional

from .rule_based_relation_extraction import RuleBasedRelationExtractor, Relation


class RelationshipExtractor:
    """High-level API that tries rule-based extraction first, optionally falling
    back to other methods (not implemented here).
    """

    def __init__(self, rule_extractor: Optional[RuleBasedRelationExtractor] = None):
        self.rule_extractor = rule_extractor or RuleBasedRelationExtractor()

    def extract(self, sentences: Iterable[str], entities_by_sentence: Iterable[Iterable[Tuple[str, str]]]) -> List[Relation]:
        """Return extracted relations from the corpus."""
        # prefer rule-based results
        results = self.rule_extractor.extract(sentences, entities_by_sentence)
        # placeholder: if rule-based returns nothing, you could add ML model here
        return results
