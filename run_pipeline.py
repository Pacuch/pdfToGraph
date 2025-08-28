"""
Command-line runner for the `text_to_graph_knowledge` package.
It accepts a JSON file (either a JSON array or JSON Lines) and runs
a simple extraction pipeline over each object, expecting a text field
in each object (default: "text"). Results are written to a JSONL file.

Example:
    python run_pipeline.py --input data/docs.json --output results.jsonl --text-field content
"""
import argparse
import json
import os
from typing import List

from text_to_graph_knowledge.input import TextInput
from text_to_graph_knowledge.named_entity_recognition import default_rule_based_ner, NERModel
from text_to_graph_knowledge.rule_based_relation_extraction import RuleBasedRelationExtractor
from text_to_graph_knowledge.relationship_extraction import RelationshipExtractor

from text_to_graph_knowledge.entity_linking import EntityLinker
from text_to_graph_knowledge.coreference_resolution import CoreferenceResolver
from text_to_graph_knowledge.co_ocurrence_graphs import CooccurrenceGraphBuilder


def load_json_objects(path: str):
    """Load objects from a JSON array file or JSON Lines file."""
    objs = []
    with open(path, "r", encoding="utf-8") as f:
        first = f.read(1)
        if not first:
            return []
        f.seek(0)

        # try to detect jsonlines (one json obj per line)
        is_json_lines = False
        with open(path, "r", encoding="utf-8") as fh:
            for _ in range(5):
                line = fh.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                if line[0] == "{" and line.endswith("}"):
                    is_json_lines = True
                    break

        if is_json_lines:
            with open(path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    objs.append(json.loads(line))
        else:
            data = json.load(f)
            if isinstance(data, list):
                objs = data
            elif isinstance(data, dict):
                objs = [data]
            else:
                raise ValueError("Unsupported JSON structure in input file.")

    return objs


def extract_entities(ner: NERModel, sentences: List[str]):
    """Run NER over each sentence and return entities_by_sentence."""
    ents_by_sentence = []
    for s in sentences:
        ents = ner.predict(s)
        ents_by_sentence.append(ents)
    return ents_by_sentence


def main():
    parser = argparse.ArgumentParser(description="Run relation extraction pipeline on JSON documents.")
    parser.add_argument("--input", "-i", required=True, help="Input JSON file (array or JSONL)")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL file with extracted relations")
    parser.add_argument("--text-field", "-t", default="text", help="JSON field containing the document text (default: 'text')")
    parser.add_argument("--kb", help="Optional path to a JSON file containing a simple KB mapping name->meta")
    parser.add_argument("--rules", help="Optional path to JSON file with rules for RuleBasedRelationExtractor")
    parser.add_argument("--window-size", type=int, default=2, help="Window size for co-occurrence graph builder")

    args = parser.parse_args()

    # Load input documents
    objs = load_json_objects(args.input)
    if not objs:
        print("No documents found in input; exiting.")
        return

    # Prepare pipeline components
    ner = default_rule_based_ner()
    coref = CoreferenceResolver()
    linker = EntityLinker()

    if args.kb and os.path.exists(args.kb):
        with open(args.kb, "r", encoding="utf-8") as fh:
            kb = json.load(fh)
        for k, v in kb.items():
            linker.add_entry(k, v)

    # Prepare rule-based extractor rules
    default_rules = [
        ("PERSON", "works_for", "ORG", [r"{L} (works at|is employed by) {R}", r"{L} works at {R}"]),
        ("PERSON", "manages", "PERSON", [r"{L} is the manager of {R}", r"{L} manages {R}"]),
    ]

    rules = default_rules
    if args.rules and os.path.exists(args.rules):
        with open(args.rules, "r", encoding="utf-8") as fh:
            user_rules = json.load(fh)
        rules = user_rules

    rule_extractor = RuleBasedRelationExtractor(rules)
    pipeline = RelationshipExtractor(rule_extractor=rule_extractor)
    graph_builder = CooccurrenceGraphBuilder(window_size=args.window_size)

    # Process documents
    with open(args.output, "w", encoding="utf-8") as out_f:
        for doc_idx, obj in enumerate(objs):
            text = obj.get(args.text_field) if isinstance(obj, dict) else None
            if not text:
                print(f"Skipping document {doc_idx}: missing field '{args.text_field}'")
                continue

            ti = TextInput.from_string(text)
            sentences = ti.split_sentences(0)

            # NER
            entities_by_sentence = extract_entities(ner, sentences)

            # Coreference
            coref_clusters = coref.resolve(sentences)

            # Entity linking
            flat_entities = set([e for sent in entities_by_sentence for e in sent])
            linked = {ent[0]: linker.link(ent[0]) for ent in flat_entities}

            # Build co-occurrence graph
            token_seqs = [ti.tokenize(s) for s in sentences]
            graph = graph_builder.build_from_tokens(token_seqs)
            top_edges = graph_builder.top_edges(10)

            # Relation extraction
            rels = pipeline.extract(sentences, entities_by_sentence)

            # Assemble output record
            out_record = {
                "doc_index": doc_idx,
                "text": text,
                "sentences": sentences,
                "entities_by_sentence": entities_by_sentence,
                "coref_clusters": coref_clusters,
                "linked_entities": linked,
                "cooccurrence_top_edges": top_edges,
                "relations": rels,
            }

            out_f.write(json.dumps(out_record, ensure_ascii=False) + "\n")
            print(f"Processed document {doc_idx}, extracted {len(rels)} relation(s).")

    print(f"Saved results to {args.output}")


if __name__ == "__main__":
    main()
