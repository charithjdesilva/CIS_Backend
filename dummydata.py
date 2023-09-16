from Security.password import hash_password,verify_password
users = []

user_login = []

user_question_table = []

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
        "photos" : 'avatar.jpg'
    }
    users.append(user)

# Print the list of objects
# for obj in dummy_list:
#     print(obj)
# This code will generate a list of 20 objects, where the Reg_No field is formatted as "IT001", "IT002", ..., "IT020", and the other fields have constant values as specified in the format. The photo_of_criminal field contains a list with a single filename for each object.






