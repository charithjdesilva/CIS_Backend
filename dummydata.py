from Security.password import hash_password,verify_password
from pathlib import Path

UPLOAD_DIR = Path() / 'users_image'


users = []

user_login = []

user_question_table = []

user_query_table = []

criminals = []

crimes = []


victims = [  
    {"crime_id": 12345,
    "life_status": "Alive",
    "nic": "98562222V",
    "first_name": "John",
    "last_name": "Due",
    "tel_no": "784561231",
    "province": "Sabaragamuwa",
    "district": "Ratnapura",
    "city": "Beliholoya",
    "area": "Pambahinna",
    "address": "",
    "landmark": "",
    "houseNoOrName": "",
    "additional_info": "",
    "photos_crime": "Images\\victim_images\\12345_98562222V.jpeg"
  }]

evidences = [
    {
    "crime_id": 12345,
    "evidence_id": 12348,
    "photo_of_evidence": "Images\\evidence_images\\common.jpg",
    "testimonials": ""
  }
]




code_in_four_digit = [i for i in range(1000,9999)]

for i in range(1,21):
    user = {
        "username" : f"user{i}",
        "password" : f"pasword{i}",
        "hash_password" : hash_password(f"password{i}")
    }
    user_login.append(user)







for i in range(1, 21):
    user = {
        "Reg_No": f"IT{i:03d}",
        "NIC": "980525364",
        "First_Name": "Alex",
        "Last_Name": "Dude",
        "Tel_No": "+9414545612",
        "Province": "Eastern",
        "City": "Kandy",
        "Area": "Kandy",
        "Address": "Main street",
        "Branch": "Kandy",
        "Position": "IOC",
        "Join_Date": "11/05/2015",
        "photo_of_user" : UPLOAD_DIR / 'avatar.png'
    }
    users.append(user)


for i in range(1, 21):
    criminal = {
        "Crime_ID": f"1{i:03d}",
        "Life Status" : "Alive",
        "In Custody" : "Yes",
        "Crime Justified" : "Yes",
        "NIC": "980525{i:03d}V",
        "First_Name": "Alex",
        "Last_Name": "Dude",
        "Tel_No": "+9414545612",
        "Province": "Eastern",
        "City": "Kandy",
        "Area": "Kandy",
        "Address": "Main street",
        "Landmark" : "",
        "photo_of_user" : UPLOAD_DIR / 'avatar.png',
        "Add to crimes" : "",
    }
    criminals.append(criminal)

# Print the list of objects
# for obj in dummy_list:
#     print(obj)
# This code will generate a list of 20 objects, where the Reg_No field is formatted as "IT001", "IT002", ..., "IT020", and the other fields have constant values as specified in the format. The photo_of_criminal field contains a list with a single filename for each object.






