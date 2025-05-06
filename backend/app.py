import os
import pandas as pd
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import HuggingFaceEmbeddings
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Global: Load your CSV file once
CSV_PATH = "product_details.csv"
df = pd.read_csv(CSV_PATH)

# Load vectorstore
VECTORSTORE_DIR = "data"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embedding_model)
retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 10})

parser = StrOutputParser()

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    docs = retriever.get_relevant_documents(user_query)

    if not docs:
        return jsonify({"error": "No results found. Try a different query."}), 404

    results = []
    for doc in docs:
        index = doc.metadata.get("index")
        if index is not None and index < len(df):
            row = df.iloc[index]
            results.append({
                "Assessment Name": row.get("Assessment Name", ""),
                "Assessment Length": row.get("Assessment Length", ""),
                "Test Type": row.get("Test Type", ""),
                "Remote Testing": row.get("Remote Testing", ""),
                "URL": row.get("URL", "")
            })

    return jsonify({"results": results})

@app.route('/', methods=['GET'])
def home():
    return "API is working fine!", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 4000))
    print(f"Starting server on port {port}...")
    app.run(host="0.0.0.0", port=port)
