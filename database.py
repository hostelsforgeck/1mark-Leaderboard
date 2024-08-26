import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from datetime import datetime



# MongoDB connection URI
uri = os.environ.get("STUDENT_LIST_URI") 
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['db1']
collection = db['S5CSD']



def save_contribution(name, contribution, team, date):
    try:
        # Find the document with the provided name
        student = collection.find_one({"name": name})

        if student:
            # Append the contribution tuple to the contributions array
            contribution_tuple = (date, contribution, team)
            if 'contributions' not in student:
                student['contributions'] = []
            student['contributions'].append(contribution_tuple)
            # Increment the number of contributions
            if 'no_of_contributions' not in student:
                student['no_of_contributions'] = 0
            student['no_of_contributions'] += 1

            # Update the document in the collection
            collection.update_one({"name": name}, {"$set": student})
            print(f"Contribution saved for name {name}")
            return True
        else:
            print(f"Student with name {name} not found")
            return False

    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def fetch_all_names_contributions():
    try:
        # Fetch all documents from the collection, including _id, name, and no_of_contributions
        documents = collection.find({}, {'_id': 1, 'name': 1, 'no_of_contributions': 1}).sort('no_of_contributions', -1)

        # Extract and return the _id, names, and contributions
        result = [(str(doc['_id']), doc['name'], doc['no_of_contributions']) for doc in documents]
        return result

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def find_details(id):
    try:
        # Convert the string ID to an ObjectId
        document = collection.find_one({"_id": ObjectId(id)}, {"name": 1, "roll_no": 1, "contributions": 1, "no_of_contributions": 1})

        if document:
            # Sort contributions by date in descending order
            contributions = document.get("contributions", [])
            sorted_contributions = sorted(contributions, key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"), reverse=True)

            # Prepare the result with necessary details
            return {
                "name": document.get("name"),
                "roll_no": document.get("roll_no"),
                "no_of_contributions": document.get("no_of_contributions"),
                "contributions": sorted_contributions
            }
        else:
            return None

    except Exception as e:
        print(f"Error occurred: {e}")
        return None




  

    





# Example usage:
# students = fetch_all_students()
# print(students)
# if students:
#     for student in students:
#         print(f"Name: {student['name']}, No. of Contributions: {student['no_of_contributions']}")
# else:
#     print("Failed to fetch students.")


# =============================================================================

# def insert_all_students(documents):
#     client = None
#     try:
#         client = MongoClient(uri, server_api=ServerApi('1'))
#         db = client['db1']
#         collection = db['S5CSD']

#         result = collection.insert_many(documents)  # Correct method is insert_many, not insertMany
#         return 1

#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return 0  # Return 0 to indicate general failure

#     finally:
#         if client:
#             client.close()


# =============================================================================


# from names import x

# count = 1
# all_list = []

# for i in x:

#     if len(str(count))==1:
#         count = f"0{count}"
        
    
#     user = {
#     "name": f"{i}",
#     "roll_no" : f"KKE22CSD0{count}",
#     "image_id":"",

#     "semester": "S5",
#     "department": "CSD",
#     "college": "GECK",

#     "contributions" : [],
#     "no_of_contributions" : 0,

#     "username" : f"KKE22CSD0{count}",
#     "password": f"KKE22CSD0{count}"
#     }

#     print(user)
#     count = int(count)
#     count+=1
#     all_list.append(user)


# insert_all_students(all_list)

# =============================================================================

# def delete_all_documents():
#     try:
#         result = collection.delete_many({})
#         print(f"Successfully deleted {result.deleted_count} documents.")
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         client.close()

# delete_all_documents()

# # =============================================================================

# def save_user(document):
#     try:
#         existing_doc = collection.find_one({"roll_no": document["roll_no"]})
#         if existing_doc:
#             return -1  # Document already exists

#         # Insert the new document
#         collection.insert_one(document)
#         return 1

#     except PyMongoError as e:
#         print(f"PyMongo error occurred: {e}")
#         return 0  # Return 0 to indicate failure due to PyMongo error

#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return 0  # Return 0 to indicate general failure

# # =============================================================================


