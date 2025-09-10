from fastapi import FastAPI
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnableSequence,RunnableLambda
import pymongo
from server_utilities import *
#creating mongo client
client = pymongo.MongoClient("mongodb://localhost:27017/")
db  = client['WorkMateCredentials']
collection= db["users id and password"]


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

#uvicorn server:app --reload
#loading chroma
load_vectore_store= Chroma(persist_directory="stores3/temple_cosine3",embedding_function=embeddings)
retriever= load_vectore_store.as_retriever(search_type="mmr",search_kwargs={"k":6})
context_chain = RunnableSequence(retriever,RunnableLambda(format_docs))

app= FastAPI()

class embedding(BaseModel):
    query : str

class database_query(BaseModel):
    user_email:str
    user_password:str = "nill"
    role:str = "nill"
    membername:str ="nill"
    member_email:str = "nill"
    user_name:str = "nill"
    field:str = "nill"
    field_value:str ="nill"
    
@app.get("/")
def home():
    return {"message":"Welcome to home page"}


"""
@app.post("/get-context")
def get_context(que:embedding):
    query = que.query
    response = context_chain.invoke(query)
    return {"message":response} 
"""
@app.post("/create-user",description= createUser)
def create_user(state:database_query):
    try :
     collection.insert_one({"_id":state.user_email,"password":state.user_password})
     return {"message":"user is created"}
    
    except Exception as e :
        return {"message": "server down"}



@app.post("/check-login",description = checkLogin)
def check_login(state:database_query):
    try:
        rec = collection.find_one({"_id":state.user_email})
        
        if rec: 
           if  rec["password"] == state.user_password:
                
                return {"message": "valid user"}
           else:
               return {"message": "invalid user"}
          
        return {"message": "no user"}
    
    except Exception as e:
        return {"message": "server down"}

@app.post("/add-group-member",description=addGroupMember)
def add_group_member(state:database_query):
    try:
       collection.update_one(
           {"_id":state.user_email},
           {"$set":{ state.role:{"name": state.membername,"email":state.member_email}}}
       )
       return {"message": "success"}
    except:
        return {"message": "failed"}
@app.post("/delete-group-member",description=deleteUser)
def delete_group_member(state:database_query):
    try:
       collection.update_one(
        {"_id": state.user_email},
        {"$unset": {state.role: ""}})
       return  {"message": "success"}
    except:
        return {"message": "failed"}

@app.post("/update-group-member",description=updateGroupMember)
def  update_group_member(state:database_query):
    try:
       rec = collection.find_one({"_id":state.user_email})
       if state.role  in rec:
           
            collection.update_one(
                {"_id":state.user_email},
                {"$set":{ state.role:{"name": state.membername,"email":state.member_email}}}
            )
        
            return  {"message": "success"}
       else :
        return   {"message": "failed"}
    except:
        return {"message": "server down"}
@app.post("/add-username",description=addUserName)
def add_user_name(state:database_query):
     try: 
      collection.update_one(
           {"_id":state.user_email},
           {"$set":{"user_name":state.user_name}})
      
      return {"message": "success"}
    
     except :
     
         return {"message": "failed"}

@app.post("/fetch-record",description=fetchRecord)
def fetch_record(state:database_query):
    try:
      rec = collection.find_one({"_id":state.user_email})
      
      return rec
    except :
        return {"message": "failed"}
@app.post("/add-new-field",description=addUserName)
def add_new_feild(state:database_query):
    try:
       collection.update_one(
    {"_id": state.user_email},             # filter condition
    {"$set": {state.field: state.field_value}}  )
       return {"message": "success"} 
    except:
        return   {"message": "failed"}
       
@app.post("/delete-field")
def delete_field(state:database_query):
    try:
       collection.update_one({"_id":state.user_email},
                             {"$unset":{state.field:""}})
       return  {"message": "success"}
    except:

         return {"message": "failed"}
