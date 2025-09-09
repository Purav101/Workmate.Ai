"""
import pymongo

st.markdown("<h1 style='color: #ff7f0e;'>Pure White</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #fafafa;'>Off White</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #e0e0e0;'>Light Gray</h3>", unsafe_allow_html=True)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db  = client['WorkMateCredentials']
collection= db["users id and password"]

                    with c2:
                      if st.button("Delete Chat",icon="🗑️"):
                        if "del_thread_id" in st.session_state:
                            
                            chat_id= st.session_state["del_thread_id"]
                            rp = delete_chat(chat_id)
                             
                            st.session_state["chat_threads"] = retrieve_all_threads()
                            if rp == True:
                                st.toast("chat deleted")
                            else: 
                                st.toast("no delte")
                            st.rerun()
"""
import sqlite3


def delete_chat(thread_id:str):
    conn = sqlite3.connect("chatbot.db",check_same_thread=False) 
    
    cursor=conn.cursor()
    try:
        cursor.execute("DELETE FROM checkpoints WHERE thread_id = ?",(thread_id,))
        cursor.execute("DELETE FROM writes WHERE thread_id = ?",(thread_id,))
        conn.commit()
        conn.close()
        return True
        # Commit changes and close connection
    except :
        conn.commit()
        conn.close()
        return False