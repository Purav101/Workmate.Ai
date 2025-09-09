import requests
from server_utilities import database_interacter,fetch_record_requester
from dbtools import dbtool
db=dbtool()
import smtplib
from langgraph.graph import StateGraph ,END,START
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,AIMessage,HumanMessage,SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from server_utilities import database_interacter
load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
# state 
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    user_email : str
    app_password:str
# making the tool
@tool
def send_email(sender_email:str,role: str, subject: str, content: str) -> dict:
    """Send email to the given role."""
    try:
        #rece = db.fetch_record(sender_email) 
        database_interacter["user_email"]= sender_email
        rece = fetch_record_requester("/fetch-record",database_interacter)
        app_passkey = rece["app_password"]
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_passkey)

        
        receiver_email = rece[role]["email"]

        text = f"Subject: {subject}\n\n{content}"
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

        return {"status": "sent", "last_receiver": receiver_email}
    except Exception as e:
        return {"status": "failed", "error": f"{str(e)} or  go to app_password not entered"}

@tool
def  get_context(query:str):
    """
    it give context of the query of the user for company,if llm not having answer,
    llm wil use this context for answering the queries
    """

    
    try:
        url ="http://127.0.0.1:8000/get-context"
        payload= {"query":query}
        #send post request
        response = requests.post(url,json=payload)
        a = dict(response.json())["message"]
        return {"context":f"{a}"}
    except Exception as e:
        return {"status": f"server not working"}
    
tools = [send_email,get_context]
llm_with_tools= llm.bind_tools(tools)

tool_node =  ToolNode(tools)

def chat_node(state:ChatState):
    messages= state['messages']
    response = llm_with_tools.invoke(messages)
    return {'messages':[response]}

#making chatbot.db to store database
conn = sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer= SqliteSaver(conn=conn)


graph = StateGraph(ChatState)
graph.add_node('chat_node',chat_node)
graph.add_node('tools',tool_node)
graph.add_edge(START,'chat_node')
graph.add_conditional_edges('chat_node',tools_condition)
graph.add_edge('tools',"chat_node")

chatbot=graph.compile(checkpointer=checkpointer)

def retrieve_all_threads()->list:
    """
    Retrieve all unique thread IDs stored in the checkpointer.

    Iterates through all available checkpoints, extracts the
    `thread_id` from each checkpoint's configuration, and returns
    them as a list of unique values.

    Returns:
        list: A list of unique thread IDs.
    """
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
