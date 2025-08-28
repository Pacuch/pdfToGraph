"""Lightweight coreference resolver using simple heuristics.

This is *not* a state-of-the-art resolver. It offers a class interface that can be
replaced with stronger backends (neural models) while keeping the rest of the
pipeline unchanged.
"""
from typing import List, Dict, Tuple
import re


class CoreferenceResolver:
    """A minimal coreference resolver.

    The resolver groups mentions into clusters. The default algorithm is a
    heuristic that links exact-string matches and resolves simple pronouns to the
    most recent compatible non-pronominal mention.
    """

    PRONOUNS = {"he", "she", "they", "it", "him", "her", "them", "his", "hers", "their"}

    def __init__(self) -> None:
        pass

    def find_mentions(self, sentences: List[str]) -> List[Tuple[int, int, str]]:
        """Return mentions as (sent_idx, token_idx, mention_text).

        This naive implementation considers any capitalized word or pronoun a mention.
        """
        mentions = []
        for si, s in enumerate(sentences):
            tokens = re.findall(r"\w+", s)
            for ti, t in enumerate(tokens):
                if t.lower() in self.PRONOUNS or t[0].isupper():
                    mentions.append((si, ti, t))
        return mentions

    def resolve(self, sentences: List[str]) -> Dict[int, List[Tuple[int, int, str]]]:
        """Resolve mentions into clusters.

        Returns a mapping cluster_id -> list of mentions.
        """
        mentions = self.find_mentions(sentences)
        clusters: Dict[int, List[Tuple[int, int, str]]] = {}
        cluster_id = 0

        # simple exact-match clustering for non-pronouns
        for m in mentions:
            si, ti, text = m
            if text.lower() not in self.PRONOUNS:
                # try to find existing cluster with same surface
                found = False
                for cid, members in clusters.items():
                    if any(m2[2] == text for m2 in members):
                        clusters[cid].append(m)
                        found = True
                        break
                if not found:
                    clusters[cluster_id] = [m]
                    cluster_id += 1

        # naive pronoun linking: assign pronouns to the most recent non-pronoun cluster
        last_non_pronoun_cluster = None
        # order mentions by position
        sorted_mentions = sorted(mentions, key=lambda x: (x[0], x[1]))
        for m in sorted_mentions:
            si, ti, text = m
            if text.lower() in self.PRONOUNS:
                if last_non_pronoun_cluster is not None:
                    clusters[last_non_pronoun_cluster].append(m)
            else:
                # find its cluster id
                for cid, members in clusters.items():
                    if any(m2[0] == si and m2[1] == ti and m2[2] == text for m2 in members):
                        last_non_pronoun_cluster = cid
                        break
        return clusters
