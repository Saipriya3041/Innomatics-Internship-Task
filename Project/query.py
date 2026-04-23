from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

retriever = db.as_retriever(search_kwargs={"k": 3})

query = input("Ask Question: ")

docs = retriever.invoke(query)

print("\nRelevant Results:\n")

for doc in docs:
    print(doc.page_content)
    print("-" * 50)