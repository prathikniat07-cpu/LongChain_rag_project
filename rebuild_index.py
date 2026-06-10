import os, sys
from pathlib import Path

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

print("Rebuilding the index using local Ollama...")

from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import shutil

docs_path = "api_docs"
db_path = "chroma_fixed_store"
embedding_model = "nomic-embed-text"
chunk_size = 800
chunk_overlap = 150

# Delete old db if it exists
if os.path.exists(db_path):
    shutil.rmtree(db_path)
    print(f"Deleted old {db_path}")

# Load documents
docs = []
p = Path(docs_path)
for f in sorted(p.glob("*.md")):
    try:
        loader = TextLoader(str(f), encoding="utf-8")
        loaded = loader.load()
        for d in loaded:
            d.metadata["source_file"] = f.name
            d.metadata["full_path"] = str(f)
        docs.extend(loaded)
        print(f"Loaded: {f.name}")
    except Exception as e:
        print(f"Skipped {f.name}: {e}")

for f in sorted(p.glob("*.pdf")):
    try:
        loader = PyPDFLoader(str(f))
        loaded = loader.load()
        for d in loaded:
            d.metadata["source_file"] = f.name
        docs.extend(loaded)
        print(f"Loaded: {f.name}")
    except Exception as e:
        print(f"Skipped {f.name}: {e}")

print(f"\nTotal documents loaded: {len(docs)}")

# Split
splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
splits = splitter.split_documents(docs)
for i, s in enumerate(splits):
    s.metadata["chunk_id"] = i

print(f"Total chunks: {len(splits)}")

# Embed and store
print("Creating embeddings with nomic-embed-text (this takes a minute)...")
embeddings = OllamaEmbeddings(model=embedding_model)
vs = Chroma.from_documents(splits, embedding=embeddings, persist_directory=db_path)

print(f"\nIndex successfully built with {len(splits)} chunks in '{db_path}'!")
print("Now refresh your Streamlit app and it will auto-load the index.")
