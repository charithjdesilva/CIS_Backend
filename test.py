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




