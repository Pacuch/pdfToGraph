import ollama

client = ollama.Client()

model = "sentence_to_cypher_llama2"
prompt = "Alice, a data scientist at OpenAnalytics, published a paper titled “Graph-based Context Tracking” with co-author Bob on June 12, 2024, and presented it at the KnowledgeGraph Summit in Berlin."

response = client.generate(model=model, prompt=prompt)

print(f"Response from Ollama {response.response}")
