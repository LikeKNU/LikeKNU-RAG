import os
from typing import List, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import numpy as np
from dotenv import load_dotenv

load_dotenv()


class KoreanEmbeddings:

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.getenv(
            "EMBEDDING_MODEL",
            "BM-K/KoSimCSE-roberta-multitask"
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)

    def get_embedding_dimension(self) -> int:
        test_embedding = self.embed_query("테스트")
        return len(test_embedding)


def embed_langchain_documents(
        documents: List[Document],
        embeddings_model: KoreanEmbeddings
) -> tuple[List[List[float]], List[str]]:
    texts = [doc.page_content for doc in documents]
    embeddings = embeddings_model.embed_documents(texts)
    return embeddings, texts


def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)

    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)

    return dot_product / (norm1 * norm2)
