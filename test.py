# # import smtplib
# # from secret123 import sender,receiver,password
# # #SERVER = "localhost"

# # FROM = sender

# # TO = [receiver] # must be a list

# # SUBJECT = "Hello!"

# # TEXT = "This message was sent with Python's smtplib."

# # # Prepare actual message

# # message = """\
# # From: %s
# # To: %s
# # Subject: %s

# # %s
# # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

# # # Send the mail

# # try:
# #     # Create an SMTP instance
# #     server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

# #     # Start TLS (Transport Layer Security) for secure communication
# #     server.starttls()

# #     # Log in to your email account
# #     server.login(sender, password)

# #     # Send the mail
# #     server.sendmail(FROM, TO, message)

# #     # Quit the server
# #     server.quit()
# #     print("Email sent successfully!")

# # except Exception as e:
# #     print(f"An error occurred: {str(e)}")


# import re

# def is_valid_password(password):
#     # Check for at least one uppercase and one lowercase letter
#     if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
#         return False

#     # Check for at least one digit and one special character
#     if not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\\-]', password):
#         return False

#     return True

# # Example usage:
# password = "MyP@ssw0rd"
# if is_valid_password(password):
#     print("Password is valid")
# else:
#     print("Password is not valid")



