import requests
import sqlite3

    
 

createUser="This endpoint creates a new user in the system. Takes email id and password  and insert into the database"
checkLogin = """Validate user credentials by checking email and password in MongoDB."""
addGroupMember =  """Update a user's MongoDB document by adding or modifying a role entry."""
deleteUser = """Remove a specific role field from a user's MongoDB document by email."""
updateGroupMember= """Upsert a role field in a user document, storing member name and email."""
fetchRecord= """Fetch a user document by email (_id) from MongoDB."""
addUserName= " add the user name "
addNew1field =   """Add or update a field in the user document."""
deleteField= """Delete a field from the user document."""
database_interacter= {"user_email":"nill",
    "user_password": "nill",
    "role": "nill",
    "membername":"nill"
,    "member_email": "nill",
    "user_name": "nill",
    "field": "nill",
    "field_value":"nill"}
def requester(end_point:str,payload:dict):
    response = requests.post(f"http://127.0.0.1:8000{end_point}",json=payload)
    a = dict(response.json())["message"]
    return a
def fetch_record_requester(end_point:str,payload:dict):
    response = requests.post(f"http://127.0.0.1:8000{end_point}",json=payload)
    a = dict(response.json())
    return a