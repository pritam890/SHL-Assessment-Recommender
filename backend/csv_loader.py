import os
import shutil
import pandas as pd
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

VECTORSTORE_DIR = "data"

def load_csv_to_documents(csv_path):
    df = pd.read_csv(csv_path)
    documents = []

    for idx, row in df.iterrows():
        content = (
            f"Assessment Name: {row['Assessment Name']}\n"
            f"Description: {row['Description']}\n"
            f"Job Levels: {row['Job Levels']}\n"
            f"Languages: {row['Languages']}\n"
            f"Assessment Length: {row['Assessment Length']}\n"
            f"Test Type: {row['Test Type']}\n"
            f"Remote Testing: {row['Remote Testing']}\n"
            f"Download Link: {row['Download Link']}\n"
            f"URL: {row['URL']}"
        )
        documents.append(Document(page_content=content, metadata={"index": idx}))
    return documents

def build_vector_store(csv_path):
    if os.path.exists(VECTORSTORE_DIR):
        print("Deleting old vectorstore...")
        shutil.rmtree(VECTORSTORE_DIR)

    print("Building vector store from CSV...")
    documents = load_csv_to_documents(csv_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(texts, embeddings, persist_directory=VECTORSTORE_DIR)
    vectordb.persist()
    print("Vector store built and persisted.")

if __name__ == "__main__":
    build_vector_store("product_details.csv")
