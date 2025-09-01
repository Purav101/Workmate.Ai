import pymongo
class dbtool:
   def new_user(self,email:str,password:str):
     """
     email : str 
     password : str
      Takes email id and password  and insert into the database
     """
     collection.insert_one({"_id":email,"password":password})
   
   def check_login(self,email:str,password:str):
        """
        Verify user credentials against the MongoDB collection.

        Looks up the user document using the provided email as the _id.
        Returns True if the document exists and the password matches,
        otherwise returns False.

        Args:
            email (str): User's email (stored as _id in MongoDB).
            password (str): User's password to validate.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        rec = collection.find_one({"_id":email})
        passscheck = False
        if rec: 
           if  rec["password"] == password:
                passscheck = True
                return True,passscheck
           else:
               return True,passscheck
            
        return False,passscheck
    
   def add_group_member(self,email:str,role:str,membername:str,member_email:str):
       """
       Input: email (str), role (str), member_email (str)
       Process: Update MongoDB document with new role key-value
       Output: None
       """
       collection.update_one(
           {"_id":email},
           {"$set":{ role:{"name": membername,"email":member_email}}}
       )
   def delete_group_member(self,email,role):
       """
        Input: email (str), role (str)
        Process: Remove the given role field from the user document identified by email
        Output: None
        """
       collection.update_one(
        {"_id": email},
        {"$unset": {role: ""}})
   def  update_group_member(self,email:str,role:str,membername:str,member_email:str):
       """
       Update (or insert if not present) a role entry for a given user document.

        This operation finds the document with the specified `_id` (email) and
        sets/updates the given `role` field to store a dictionary containing
        the member's name and email.

        Args:
            email (str): The unique identifier (`_id`) of the user document.
            role (str): The role field name to be updated in the document.
            membername (str): The member's display name.
            member_email (str): The member's email address.

        Effect:
            - If the document with `_id=email` exists, the `role` field is
            updated with the provided details.
            - If the `role` field does not exist, it will be created.
       """
       collection.update_one(
           {"_id":email},
           {"$set":{ role:{"name": membername,"email":member_email}}}
       )
       
   def add_user_name(self,email:str,user_name:str):
      """
        Add or update a user's name in the database.

        This method updates the document identified by the given `email`
        (`_id` in the collection) and sets its `user_name` field to the
        provided value.

        Args:
            email (str): The unique identifier (`_id`) of the user document.
            user_name (str): The name to assign to the user.

        Returns:
            UpdateResult: The result of th    e update operation, which includes
            information such as `matched_count` and `modified_count`.
       """
       
      collection.update_one(
           {"_id":email},
           {"$set":{"user_name":user_name}})
        
   def fetch_record(self,email:str):
       
      rec = collection.find_one({"_id":email})
      
      return rec
    
   def add_new_feild(self,email:str,field:str,value:str):
       collection.update_one(
    {"_id": email},             # filter condition
    {"$set": {field: value}}  # new field
)      
   def delete_field(self,email:str,field:str):
       collection.update_one({"_id":email},
                             {"$unset":{field:""}})





#if __name__ == "__main__":
    #print("Welcome to pymongo")
client = pymongo.MongoClient("mongodb://localhost:27017/")
    #print(client)
db  = client['WorkMateCredentials']
collection= db["users id and password"]
#collection.insert_one({"user_name":"Purav","password":"1234"})
    #all_docs= collection.find({'name':"Purav"})
    #or item in all_docs:
        
     # print(item)
     
   # alldbs = client.list_database_names()
    #print(alldbs)
   #