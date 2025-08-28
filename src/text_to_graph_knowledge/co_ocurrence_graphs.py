"""Build co-occurrence graphs from token or entity sequences.

The implementation uses networkx if available, otherwise falls back to a
simple adjacency dict structure.
"""
from typing import Iterable, List, Tuple, Dict
try:
    import networkx as nx  # optional
except Exception:
    nx = None


class CooccurrenceGraphBuilder:
    """Create co-occurrence graphs using a sliding window.

    Parameters
    ----------
    window_size : int
        Number of tokens to consider for co-occurrence.
    use_networkx : bool
        Prefer networkx if available.
    """

    def __init__(self, window_size: int = 2, use_networkx: bool = True) -> None:
        self.window_size = max(1, int(window_size))
        self._use_nx = use_networkx and (nx is not None)
        self._graph = None

    def build_from_tokens(self, token_sequences: Iterable[List[str]]):
        if self._use_nx:
            G = nx.Graph()
            for tokens in token_sequences:
                n = len(tokens)
                for i in range(n):
                    for j in range(i + 1, min(i + 1 + self.window_size, n)):
                        a, b = tokens[i], tokens[j]
                        if G.has_edge(a, b):
                            G[a][b]["weight"] += 1
                        else:
                            G.add_edge(a, b, weight=1)
            self._graph = G
        else:
            adj: Dict[str, Dict[str, int]] = {}
            for tokens in token_sequences:
                n = len(tokens)
                for i in range(n):
                    for j in range(i + 1, min(i + 1 + self.window_size, n)):
                        a, b = tokens[i], tokens[j]
                        adj.setdefault(a, {}).setdefault(b, 0)
                        adj.setdefault(b, {}).setdefault(a, 0)
                        adj[a][b] += 1
                        adj[b][a] += 1
            self._graph = adj
        return self._graph

    def get_graph(self):
        return self._graph

    def top_edges(self, k: int = 10):
        """Return top-k edges by weight as list of ((u, v), weight)."""
        if self._graph is None:
            return []
        if self._use_nx:
            edges = sorted(self._graph.edges(data=True), key=lambda e: e[2].get("weight", 1), reverse=True)
            return [((u, v), d.get("weight", 1)) for u, v, d in edges[:k]]
        else:
            pairs: List[Tuple[Tuple[str, str], int]] = []
            seen = set()
            for u, nbrs in self._graph.items():
                for v, w in nbrs.items():
                    if (v, u) in seen:
                        continue
                    seen.add((u, v))
                    pairs.append(((u, v), w))
            pairs.sort(key=lambda x: x[1], reverse=True)
            return pairs[:k]
