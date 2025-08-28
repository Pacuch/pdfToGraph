"""A rule-based relation extractor using simple pattern templates.

Rules are tuples of (left_label, relation_label, right_label, textual_patterns),
where textual_patterns may contain placeholders {L} and {R} to be substituted by
regexes that capture entity surfaces.
"""
from typing import List, Tuple, Dict, Iterable
import re

Relation = Tuple[str, str, str]  # (left_text, relation_label, right_text)


class RuleBasedRelationExtractor:
    """Rule-based extractor with pluggable textual patterns.

    Example rule:
        ("PERSON", "works_for", "ORG", [r"{L} works at {R}", r"{L} is employed by {R}"])
    """

    def __init__(self, rules: Iterable[Tuple[str, str, str, Iterable[str]]] = ()):  # label-label-text patterns
        self.rules = []
        for left_label, rel_label, right_label, patterns in rules:
            compiled = [re.compile(p.replace("{L}", r"(?P<L>.+?)").replace("{R}", r"(?P<R>.+?)"), re.I) for p in patterns]
            self.rules.append((left_label, rel_label, right_label, compiled))

    def extract_from_sentence(self, sentence: str, entities: Iterable[Tuple[str, str]]) -> List[Relation]:
        """Extract relations from a single sentence.

        `entities` is an iterable of (entity_text, entity_label).
        """
        results: List[Relation] = []
        # build quick lookup by surface lowercased
        ent_map: Dict[str, List[str]] = {}
        for surf, label in entities:
            ent_map.setdefault(surf.lower(), []).append(label)

        for left_label, rel_label, right_label, patterns in self.rules:
            for pat in patterns:
                for m in pat.finditer(sentence):
                    L = m.groupdict().get("L", "").strip()
                    R = m.groupdict().get("R", "").strip()
                    if not L or not R:
                        continue
                    # verify that the extracted L and R match the requested entity labels
                    L_labels = ent_map.get(L.lower(), [])
                    R_labels = ent_map.get(R.lower(), [])
                    if (not left_label or left_label in L_labels) and (not right_label or right_label in R_labels):
                        results.append((L, rel_label, R))
        return results

    def extract(self, sentences: Iterable[str], entities_by_sentence: Iterable[Iterable[Tuple[str, str]]]) -> List[Relation]:
        all_rels: List[Relation] = []
        for s, ents in zip(sentences, entities_by_sentence):
            all_rels.extend(self.extract_from_sentence(s, ents))
        return all_rels
