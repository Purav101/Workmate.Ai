from fastapi import FastAPI
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnableSequence,RunnableLambda

def format_docs(retrieved_docs):
    """
    
    """
    context_text="\n\n".join(doc.page_content for doc in retrieved_docs )
    return context_text


#initializing model
#initializing embeddings model
model_name ="BAAI/bge-large-en"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings':False}
embeddings =  HuggingFaceEmbeddings(
    model_name = model_name,
    model_kwargs = model_kwargs,
    encode_kwargs = encode_kwargs 
)

#loading chroma
load_vectore_store= Chroma(persist_directory="stores3/temple_cosine3",embedding_function=embeddings)
retriever= load_vectore_store.as_retriever(search_type="mmr",search_kwargs={"k":6})
context_chain = RunnableSequence(retriever,RunnableLambda(format_docs))

app= FastAPI()

class embedding(BaseModel):
    query : str

@app.post("/get-context")
def get_context(que:embedding):
    query = que.query
    response = context_chain.invoke(query)
    return {"message":response} 