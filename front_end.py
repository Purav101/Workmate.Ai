import requests
import re
from server_utilities import database_interacter,requester,fetch_record_requester
import streamlit as st
from test import delete_chat
from dbtools import dbtool
db = dbtool()
import pandas as pd
from architecture import chatbot,retrieve_all_threads
from langchain_core.messages import BaseMessage,AIMessage,HumanMessage,SystemMessage,ToolMessage
import uuid
from prompts import email_prompt
#setting user email for requester
if "user_email" in st.session_state:
  database_interacter["user_email"] = st.session_state["user_email"]
# utilities
def generate_thread_id():
    return uuid.uuid4()


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)
def reset_chat():
    """
    whenever user click on the new chat button 
    it reset the chat 
    """
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable":{"thread_id":thread_id}})
    # check if messages key exist or not 
    return state.values.get("messages",[])


#Related to chat bot  session
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in  st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] =  retrieve_all_threads()

add_thread(st.session_state["thread_id"])


c=0

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Function to switch page
def switch_page(page_name):
    st.session_state.page = page_name
# Simple user storage (in memory)
if 'users' not in st.session_state:
    st.session_state.users = {}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def main():
    
    
    if st.session_state.logged_in:
        
        #after login homepage
        st.sidebar.button("🏠 Home", on_click=switch_page, args=("Home",))
        st.sidebar.button("🤖 Your work mate", on_click=switch_page, args=("Tasks",))
        st.sidebar.button("Previous chats", on_click=switch_page, args=("history",))
        st.sidebar.button("⚙️ Settings", on_click=switch_page, args=("details",))
        

                # Render pages based on session_state.page
                #LOGIN PAGE
        if st.session_state.page == "Home":
                    if st.session_state["lin"]:
                        st.toast("Welcome! You are logged in.",icon="✅")
                        st.session_state["lin"]= False
                    
                    st.title("Welcome to WorkMate.AI")
                    st.write("Choose a feature from the sidebar.")
                    
                    #controlling the username
                    if "username" not in st.session_state:
                        
                        name = st.text_input("What is your name ?")
                        #in home db add user name 
                        st.session_state["username"] = name
                        database_interacter["user_email"] = st.session_state["user_email"]
                        database_interacter["user_name"] = name
                        res = requester("/add-username",database_interacter)
                        
                    
                    
                    
                    # add member form 
                    st.title("Add  Team Member 👥")

                    # Three input fields
                    role = st.text_input("Role 🧑‍💼")
                    name = st.text_input("Name") 
                    eaddress = st.text_input("E-mail Address 📧")

                    # Buttons
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if st.button("Add"):
                            
                            if role and name and eaddress:
                                    
                                    check = fetch_record_requester("/fetch-record",database_interacter)
                                    if role not in check:
                                        database_interacter["role"]= role
                                        database_interacter["membername"] = name
                                        database_interacter["member_email"] = eaddress
                                        rec = requester("/add-group-member",database_interacter)
                                        if rec == "success":
                                            st.toast(f"{name}({role}) added!",icon="✅")
                                        else:
                                            st.toast("Please try again later 🛑")
                                    else :
                                      st.toast(f"{role} role already exists ⚠️")
                            else:
                                st.toast("Fill all the fields ⚠️")
                             
                             
                                    
                    with col2:
                        if st.button("Update"):
                            
                           
                            if role and name and eaddress:
                                
                                database_interacter["role"]= role
                                database_interacter["membername"] = name
                                database_interacter["member_email"] = eaddress
                                res = requester("/update-group-member",database_interacter)  
                                if res == "success":
                                    st.toast(f"{name}({role}) updated!",icon="✅")
                                elif res == "failed" :
                                    st.toast(f"{role} not exists!",icon="⚠️")    
                                else:
                                    st.toast("Please try again later",icon="🚫")
                            else: 
                                st.toast("Fill all the fields",icon="⚠️")
                    
                    
                    
                    
                    with col3:
                        if st.button("Delete Role"):
                            
                            if not role :
                                st.toast("Enter the role",icon="⚠️")       
                                   
                            if name and eaddress :
                                st.toast(f"do not enter name and email address",icon="⚠️")       
                            else:
                                rec = fetch_record_requester("/fetch-record",database_interacter)
                                if role  in rec:
                                    database_interacter["role"] = role
                                    res = requester("/delete-group-member",database_interacter)
                                    if res == "success":
                                       st.toast(f"{role} deleted !",icon="✅")       
                                    else:
                                        st.toast(f"failed to delete !",icon="⚠️")
                                else:
                                    st.toast(f"{role} not exists !",icon="⚠️")
                                
                    
                   
                   
                   
                   
                    # printing the names
                    st.title("Your Team Member 👥")
                    rec = fetch_record_requester("/fetch-record",database_interacter)
                    
                    if len(rec) > 3:
                        data = []
                        for key in rec.keys():
                            if key != '_id' and key != "password" and key != "user_name" and key != "app_password":
                                tdict = {"Role 👨‍💻":key,"Name":rec[key]["name"],"E-mail": rec[key]["email"]}
                                data.append(tdict)
                        # making df
                        df = pd.DataFrame(data)[["Role 👨‍💻","Name","E-mail"]]
                        # Shift index to start from 1
                        df.index = df.index + 1
                        df.index.name = "S.No"   # optional, gives a label to index column

                        st.table(df)
                        
        #settings page     

        elif st.session_state.page == "details":
                    st.title("⚙️ Settings")
                    st.write("This information is for personalized experience !!")
                    st.write("Once you log out this information is deleted !!")
                    
                    st.subheader("🔐 Set your details")
                    app_password = st.text_input(" Gmail App password :", key="login_user")
                           
                    if st.button("Submit"):
                        if app_password:
                                database_interacter["field"] = "app_password"
                                database_interacter["field_value"] = app_password
                                res = requester("/add-new-field",database_interacter)
                                st.success("App password saved")
                        else:
                            st.toast("Fill the field",icon="⚠️")
                    if st.button("Help ?"):
                        st.success(""" 🔒 Note: Make sure Two-Factor Authentication (2FA) is enabled on your Google account.
Then search for “App Password” in your Google Account settings.
Generate an App Password for your email ID and use it here instead of your normal Gmail password.""")
                    #logout button
                    if st.button("Logout"):
                        database_interacter["field"] = app_password
                        res = requester("/delete-field",database_interacter)
                        st.session_state.logged_in = False
                        st.session_state.pop("username", None)
                        
                        st.rerun()        
                
                
                
                
                # TASK EXECUTER
        
        
        
        
        
        
        elif st.session_state.page == "Tasks":
                    st.title("I am your task agent ")
                    
                    
                    
                    st.sidebar.header("📜 Previous Chats")
                    # for align side by side
                    c1,c2 = st.sidebar.columns(2)
                    with c1:
                      if st.button("New Chat",icon="➕"):
                                reset_chat()
                    with c2:
                          
                        if st.button("Delete Chat",icon="🗑️"):
                            d =  delete_chat(st.session_state["thread_id"])
                            st.session_state["chat_threads"].remove(st.session_state["thread_id"])
                            st.session_state["thread_id"]= st.session_state["chat_threads"][-1]
                            if d:
                                st.toast("deleted") 
                            st.rerun()
                    #loading the old chats
                    for thread_id in st.session_state["chat_threads"][::-1]:
                        
                        
                        
                        if st.sidebar.button(str(thread_id)):
                            
                            st.session_state["thread_id"] = thread_id
                            
                            messages = load_conversation(thread_id)
                            
                            #loading all the messages related to the thread_id
                            
                            temp_messages = []
                            for msg in messages :
                                role = "user" 
                                if isinstance(msg,HumanMessage):
                                    role = "user"
                                    temp_messages.append({"role":role,"content":msg.content})
                                elif isinstance(msg,AIMessage):
                                   role = "assistant"
                                   temp_messages.append({"role":role,"content":msg.content})
                            st.session_state["message_history"] = temp_messages
                     
                    # Printing  the all chat message
                    for message in st.session_state["message_history"]:
                        with st.chat_message(message["role"]):
                           #st.text(message["content"]) 
                           cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", message["content"])  # remove bold
                           cleaned = re.sub(r"[*#-]", "", cleaned)                        # remove bullets/headings
                    
                           st.text(cleaned)
                    
                    user_input = st.chat_input("Type here !")
                    
                           
                    if user_input:
                        #show users message
                        st.session_state["message_history"].append({"role":"user","content":user_input})
                        with st.chat_message("user"):
                            st.text(user_input)
                        CONFIG = {
                            "configurable":{"thread_id":st.session_state["thread_id"]},
                            "meatdata" :{"thread_id": st.session_state["thread_id"]},
                            "run_name" : {"chat_turn"},
                        }
                        with st.chat_message("assistant"):
                            #Use a mutable holder so that the generator can set/modify it 
                            status_holder = {"box":None}
                            def ai_message_streaming():
                                for message_chunk,metadata  in chatbot.stream({
                                    "messages":[HumanMessage(content = user_input),SystemMessage(content=email_prompt),SystemMessage(content= f"sender email address is {st.session_state["user_email"]} ")]},
                                    #,SystemMessage(content=email_prompt),SystemMessage(content= f"sender email address is {st.session_state["user_email"]} ")
                                    config= CONFIG,
                                    stream_mode= "messages",
                                           ):
                                    # laz loading for updating the status barr
                                    if isinstance(message_chunk,ToolMessage):
                                      
                                        tool_name= getattr(message_chunk,"name","tool")
                                      
                                        if status_holder["box"] is None:
                                           status_holder["box"]= st.status(f"🛠️ Using {tool_name}....",expanded=True)
                                        else:
                                            status_holder["box"].update(
                                                label=f"🛠️ Using {tool_name}.....",
                                                state="running",
                                                expanded =True
                                            )
                                    #stream only asssistant tokens
                                    if isinstance(message_chunk,AIMessage):
                                        yield message_chunk.content
                            
                            ai_message= st.write_stream(ai_message_streaming())
                            
                            #finalize only if tool is used
                            if status_holder["box"] is not None:
                                status_holder["box"].update(
                                    label = "✅ Tool finished",state="complete",expanded=False
                                )
                        st.session_state["message_history"].append(
                            {"role":"assistant","content":ai_message}
                        )
        
        
        
        elif st.session_state.page == "history":
                    st.title("control chats")
                    st.write("work on progress")
                    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    else:
        st.title("Login Form")
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.subheader("Sign In")
            usernameid = st.text_input("E-mail Address", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            database_interacter["user_email"] = usernameid
            database_interacter["user_password"] = password
            if st.button("Login"):
                res=requester("/check-login",database_interacter)
                if usernameid and password:
                    if res == "valid user":
                        st.session_state.logged_in = True
                        st.success("Login successful!")
                        st.session_state["user_email"] = usernameid
                        c= st.session_state["user_email"]
                        st.session_state["lin"] = True
                        st.rerun() 
                    elif res == "invalid user":
                        st.error("Wrong password")
                    elif res == "no user":
                        st.error("Sign up first !!")
                    elif res == "server down" : 
                        st.error("Please try again later !!")
                else:
                    st.error("Fill all the fields")
        
        with tab2:
            st.subheader("Sign Up")
            new_usernameid = st.text_input("E-mail", key="signup_user")
            new_password = st.text_input("Password", type="password", key="signup_pass")
            database_interacter["user_email"] = new_usernameid
            database_interacter["user_password"] = new_password
            #hit api
            if st.button("Sign Up"):
                if new_usernameid and new_password:
                    a=requester("/check-login",database_interacter)
                    
                    if a == "no user":
                        a = requester("/create-user",database_interacter)
                
                        
                        if a != "server down":
                           st.success("Account created! You can now sign in.")
                        else:
                           st.error("please try again later")         
                    else:
                        st.error("E-mail id  already exists")
                else:
                    st.error("Please fill all fields")

if __name__ == "__main__":
    main()