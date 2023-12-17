# # # import smtplib
# # # from secret123 import sender,receiver,password
# # # #SERVER = "localhost"

# # # FROM = sender

# # # TO = [receiver] # must be a list

# # # SUBJECT = "Hello!"

# # # TEXT = "This message was sent with Python's smtplib."

# # # # Prepare actual message

# # # message = """\
# # # From: %s
# # # To: %s
# # # Subject: %s

# # # %s
# # # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

# # # # Send the mail

# # # try:
# # #     # Create an SMTP instance
# # #     server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

# # #     # Start TLS (Transport Layer Security) for secure communication
# # #     server.starttls()

# # #     # Log in to your email account
# # #     server.login(sender, password)

# # #     # Send the mail
# # #     server.sendmail(FROM, TO, message)

# # #     # Quit the server
# # #     server.quit()
# # #     print("Email sent successfully!")

# # # except Exception as e:
# # #     print(f"An error occurred: {str(e)}")


# # import re

# # def is_valid_password(password):
# #     # Check for at least one uppercase and one lowercase letter
# #     if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
# #         return False

# #     # Check for at least one digit and one special character
# #     if not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\\-]', password):
# #         return False

# #     return True

# # # Example usage:
# # password = "MyP@ssw0rd"
# # if is_valid_password(password):
# #     print("Password is valid")
# # else:
# #     print("Password is not valid")

# import random
# from faker import Faker

# # Create a Faker instance with the 'lk_LK' locale for Sri Lankan-style data
# fake = Faker()

# # Generate a random Sri Lankan mobile phone number
# def generate_sri_lankan_mobile_number():
#     # Sri Lankan mobile operator codes and their respective lengths
#     operator_codes = {
#         "Dialog": 77,
#         "Mobitel": 71,
#         "Airtel": 75,
#         "Hutch": 78,
#         "Etisalat": 72,
#         # Add more operator codes as needed
#     }
    
#     # Choose a random mobile operator code
#     operator = random.choice(list(operator_codes.keys()))
    
#     # Generate the subscriber number with the remaining digits
#     subscriber_number = ''.join(random.choices("0123456789", k=9 - operator_codes[operator]))
    
#     # Format the mobile number
#     mobile_number = f"0{operator_codes[operator]}{subscriber_number}"
    
#     return mobile_number

# # # Generate and print a random Sri Lankan mobile phone number
# # random_mobile_number = generate_sri_lankan_mobile_number()
# # print("Random Sri Lankan Mobile Number:", random_mobile_number)

# def generate_sri_lankan_nic():
#     return fake.random_int(min=1000000000, max=9999999999)

# sri_lankan_provinces = [
#     "Western",
#     "Central",
#     "Southern",
#     "Northern",
#     "Eastern",
#     "North Western",
#     "North Central",
#     "Uva",
#     "Sabaragamuwa"
# ]

# # Generate 50 random dictionaries
# random_dicts = []
# for _ in range(50):
#     random_dict = {
#         "Reg_No": fake.random_int(min=1000, max=9999),
#         "NIC": generate_sri_lankan_nic(),
#         "First_Name": fake.first_name(),
#         "Last_Name": fake.last_name(),
#         "Tel_No": generate_sri_lankan_mobile_number(),
#         "Province": random.choice(sri_lankan_provinces),
#         "City": fake.city(),
#         "Area": fake.street_name(),
#         "Address": fake.street_address(),
#         "Branch": fake.company(),
#         "Position": fake.job(),
#         "Join_Date": fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y-%m-%d"),
#         "photo_of_criminal": [
#             {
#                 "url": fake.image_url(),
#                 "name": fake.word()
#             }
#         ]
#     }
#     random_dicts.append(random_dict)

# # Print the generated dictionaries
# # for idx, random_dict in enumerate(random_dicts, start=1):
# #     print(f"Dictionary {idx}:")
# #     print(random_dict)
# #     print("\n")
# print(random_dicts)


# # The string to search in
# full_string = r"Images\users_image\924564581V_CRM0003.jpeg"

# # The substring to check for
# substring = "CRM0003"

# # Check if the substring exists in the full string
# if substring in full_string:
#     print(f"'{substring}' is present in '{full_string}'.")
# else:
#     print(f"'{substring}' is not present in '{full_string}'.")

# base_url = "http://127.0.0.1:8000"  # Replace with your actual base URL
# file_path = "Images\\victim_images\\VID_2020_10_V1.jpeg"  # Replace with your actual file path

# # Convert backslashes to forward slashes and remove leading slashes
# file_path = file_path.replace("\\", "/").lstrip("/")

# # Combine the base URL and file path to create the complete URL
# url = f"{base_url}/{file_path}"

# # print(url)

# def make_image_url(file_path : str):
#     file_path = file_path.replace("\\", "/").lstrip("/")
#     return f"{base_url}/{file_path}"


# from urllib.parse import urlparse
# import os

# url = "http://127.0.0.1:8000/Images/crime_images/CR_2020_10_C3.jpg"
# parsed_url = urlparse(url)
# filename = os.path.basename(parsed_url.path)

# print(filename)
# print(url.split('/')[-1])

# path = "Images\\users_image\\753951456V.jpeg"
# corrected_path = path.replace('\\\\', '//')
# print(corrected_path)


# path = "Images\\users_image\\753951456V.jpeg"
# converted_path = path.replace('\\', '/')
# print(converted_path)

text = "http://127.0.0.1:8000/Images/crime_images/CR_2021_08_14_C1_1.jpeg~http://127.0.0.1:8000/Images/crime_images/CR_2021_08_14_C1_2.jpeg~"

l1 = text.split("~")

print(l1)

print("CR_2021_08_14_C1" in  "http://127.0.0.1:8000/Images/crime_images/CR_2021_08_14_C1_1.jpeg~http://127.0.0.1:8000/Images/crime_images/CR_2021_08_14_C1_2.jpeg~")





# @router.post('/register/crime/multiple_photos')
# async def register_crime_with_multiple_photos(
#     db: db_dependency,
#     CrimeID: Annotated[str, Form()],
#     CrimeType: Annotated[str, Form()],
#     CrimeDate: Annotated[str, Form()],
#     CrimeTime: Annotated[str, Form()],
#     Province: Annotated[str, Form()],
#     District: Annotated[str, Form()],
#     City: Annotated[str, Form()],
#     Area: Annotated[str, Form()],
#     Landmarks: Annotated[str, Form()] = None,
#     HouseNoOrName: Annotated[str, Form()] = None,
#     testimonials: Annotated[str, Form()] = None,
#     photos_crime: List[UploadFile] = File(...)
# ):
#     if CrimeDate:
#         joined_date = datetime.strptime(CrimeDate, '%Y-%m-%d')
#     else:
#         joined_date = None

#     img_url = ""

#     crime = Crime(
#         CrimeID=CrimeID,
#         CrimeType=CrimeType,
#         CrimeDate=joined_date,
#         CrimeTime=CrimeTime,
#         Province=Province,
#         District=District,
#         City=City,
#         Area=Area,
#         HouseNoOrName=HouseNoOrName,
#         Landmarks=Landmarks,
#         Testimonials=testimonials
#     )

#     try:
#         db.add(crime)
#         db.commit()
#         db.refresh(crime)

        
#     except Exception as e:
#         error_message = str(e)
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


#     for index,photo in enumerate(photos_crime):
#             upload_img_url = await upload_image_with_multiple_photos(photo, CrimeID, UPLOAD_CRIME,index) 
#             img_url = upload_img_url 
#             photo = Photos(
#                 PhotoID=f"{CrimeID}%{index}",
#                 PhotoType="Crime",
#                 PhotoPath=img_url
#             )

#             try:
#                 db.add(photo)
#                 db.commit()
#                 db.refresh(photo)
        
#             except Exception as e:
#                 error_message = str(e)
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")

#             crime_photo = CrimePhoto(
#                 PhotoID=f"{CrimeID}%{index}",
#                 CrimeID=CrimeID
#             ) 

#             try:
#                 db.add(crime_photo)
#                 db.commit()
#                 db.refresh(crime_photo)

        
#             except Exception as e:
#                 error_message = str(e)
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
            

#     return status.HTTP_201_CREATED


t1 = "20231217003%1.jpeg"

print(t1.split(".")[0])








