from typing import List, Tuple, Dict, Iterable
import re


Entity = Tuple[str, str]

class NERModel:
    """Named Entity Recognition interface and a small rule-based implementation.

    Methods
    -------
    train(corpus)
        Placeholder.
    predict(text)
        Return list of (entity_text, label) tuples.
    """

    def __init__(self, rules: Iterable[Tuple[str, str]] = ()):  # regex pattern -> label
        # compile rules (pattern, label)
        self.rules = [(re.compile(p), lbl) for p, lbl in rules]

    def train(self, *args, **kwargs):
        """Optional training method for pluggable models. Not implemented in rule-based version."""
        raise NotImplementedError("Training is backend-specific. Use a subclass that implements train().")

    def predict(self, text: str) -> List[Entity]:
        """Perform entity recognition using the configured regex rules.

        Returns
        -------
        List[Tuple[str, str]]
            Sequence of (matched_text, label).
        """
        entities: List[Entity] = []
        for pattern, label in self.rules:
            for m in pattern.finditer(text):
                entities.append((m.group(0), label))
        return entities


# small factory for quick use
def default_rule_based_ner() -> NERModel:
    rules = [
        (r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b", "PERSON"),  # simple two-name rule
        (r"\b[A-Z][a-z]+\b", "PROPER_NOUN"),
        (r"\b\d{4}\b", "DATE"),
    ]
    return NERModel(rules=rules)
