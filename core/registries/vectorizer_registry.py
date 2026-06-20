from core.registries.component_registry import ComponentRegistry


VECTORIZERS = ComponentRegistry("vectorizer")
VECTORIZERS.register(
    "sentence_transformer",
    "implementations.vectorizers.sentence_transformer_vectorizer:"
    "SentenceTransformerVectorizer",
)
