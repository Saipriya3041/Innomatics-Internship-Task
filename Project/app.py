from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

retriever = db.as_retriever(search_kwargs={"k": 2})

query = input("Ask Support Question: ")

docs = retriever.invoke(query)

if docs:
    print("\nAnswer:")
    print(docs[0].page_content)
else:
    print("No answer found.")