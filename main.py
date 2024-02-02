import time
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

loggedin = None # <-- Let's us store a user's details locally


def menu():
  global loggedin

  if loggedin is None:
    
    '''  
      Shows a basic "Start" menu if the user is not logged in or if the "loggedin" global variable is empty
    '''
    
    print("Welcome to the Start Menu"'\n')
    print("1. Login"'\n'"2. Register"'\n'"3. Reset Password"'\n'"4. Exit Program"'\n')
    
    option = input("> ")

    if option == "1":
      login()
    elif option == "2":
      register()
    elif option == "3":
      reset()
    elif option == "4":
      print("Goodbye. . .")
    else:
      print("Invalid option. . .")
      menu()

  else:
    if loggedin['role'] == 'user':
      
      '''  
        Shows a basic user portal if the user is logged in and only has the role "user"
      '''
      
      print('\n'"-----------------------"'\n'"Welcome to the User Portal!"'\n')
      print('1. View Profile''\n''2. Change Password''\n''3. Change Email''\n''4. Logout''\n')
      option = input("> ")

      if option == "1":
          profile()
      elif option == "2":
          change_pass()
      elif option == "3":
          change_email()
      elif option == "4":
          print("Signing Out. . .")
          loggedin = None
          menu()
      else:
          print("Invalid Option. . .")
          menu()

    elif loggedin['role'] == 'admin':
      
      '''  
        Shows a basic admin portal if the user is logged in and they hold only the role "admin"

        The options:

            - Delete User
            - Change Role
            - Change User Password

            Are admin specific functions. User's will not be able to view this menu nor choose these options.
      '''
      
      print('\n'"---------------------"'\n'"Welcome to the Admin Portal"'\n')
      print('1. View Profile''\n''2. Change Password''\n''3. Change User Password''\n''4. Change Role''\n''5. Delete User''\n''6. Logout''\n')

    option = input("> ")

    
    if option == "1":
      profile()
    elif option == "2":
      change_pass()
    elif option == "3":
      change_user_pass()
    elif option == "4":
      change_role()
    elif option == "5":
      delete_user()
    elif option == "6":
      print("Signing Out. . .")
      loggedin = None
      menu()
    else:
      print("Invalid Option. . .")
      menu()

def login(): # <--- Script for User Login
  
  '''
    This function is the login script. This allows a secure way for users to login with the following features:

        - Password Masking
        - Username and Password Checking

        All these functions allow a semi secure login experience
  '''
  
  global loggedin

  username = input("Username: ")
  password = input("Password: ")

  if user_exists(username) and check_password(username, password):
    # ^^^^ Calls on two scripts to check entered details against data file
    print("Login Authorised! Signing in. . ."'\n')
    loggedin = {'username': username, 'role': get_user_role(username), "status": get_user_status(username)} # Stores info for the global variable "loggedin"
    time.sleep(2)
    menu()

  else: # <--- If there password or username are invalid
    print("Invalid Username or Password. . ."'\n')
    login()


def register(): # <-- Script for Registering Users
  # Requests the user to enter a username and password
  username = input("Username: ") 
  password = input("Password: ")

  if user_exists(username): # <--- Checks if the username entered already exists
    print("User with that username already exists!")
    register()
  else: # <--- If the username isn't in the text file
    email = input("Email: ") # <--- Requests the user to enter an email and stores it locally
    code = str(generate_code()) # <--- Calls on function to create a 6 digit code
    userrole = 'user' # <--- Tells the code to give the account "user" access

    send_email(username, email, code) # <--- Calls on function "send_email" to send the verification code

    print("An email with a verification code has been sent to the email address entered! Please enter it below!")

    verify_code = input("> ")

    if verify_code == code: # <--- Checks if the verification code entered matches the generated code
      status = 'verified'
      register_user(username, password, userrole, status, email)
      print("Processing. . .  Please Wait!")
      time.sleep(2)
      print("Account Registered!"'\n'"Taking you to login. . ."'\n')
      login()
    else: # <--- If the code doesn't match
      print("Verification Failed! Invalid Code!"'\n')
      register()

      
def reset():
  username = input("Username: ")

  if user_exists(username):
    email = input("Your Registered Email: ")

    if check_email(username, email):
      code = str(generate_code())

      send_email(username, email, code)

      print("For security, please enter the 6 digit code sent to your registered email!")

      entercode = input("> ")

      if entercode == code:
        new_password = input("New Password: ")
        
        update_password(username, new_password)
        print("Processing. . .  Please Wait!")
        time.sleep(2)
        print("Your password has been reset!"'\n')
        menu()
      else:
        print("Invalid Code Entered, Returning to menu!"'\n')
        menu()

    else:
      print("Invalid Email, Returning to menu!"'\n')
      menu()

  else:
    print("User does not exist, Returning to menu!")
    menu()


def change_pass():
  global loggedin

  password = input("Current Password: ")

  if check_password(loggedin['username'], password):
    new_password = input("New Password: ")
    update_password(loggedin['username'], new_password)
    print("Processing. . .  Please Wait!")
    time.sleep(2)
    print("Password has been updated")
    menu()

  else:
    print("Current Password is incorrect!")
    change_pass()

def change_email():
  global loggedin

  new_email = input("New Email: ")

  update_email(loggedin['username'], new_email)
  print("Processing. . .  Please Wait!")
  time.sleep(2)
  print("Email updated successfully!")
  menu()

def profile():
  global loggedin

  print("Getting Details. . .")
  time.sleep(2)

  print(f'Username: {loggedin["username"]}'"\n")
  print(f'Auth Level: {loggedin["role"]}'"\n")
  print(f'Email: {get_email(loggedin["username"])}'"\n")
  print(f'Status: {loggedin["status"]}'"\n")
  
  time.sleep(3)
  menu()



def change_user_pass():
  # Admin Only
  username = input("Username: ")

  if user_exists(username): # <-- checks if the user exists
    new_password = input("New Password: ")
    update_password(username, new_password)
    print("Processing. . .  Please Wait!")
    time.sleep(2)
    print(f"User password for {username} has now been updated!")
    menu()

  else:
    print(f'Processing. . . Please Wait!')
    time.sleep(2)
    print(f'User {username} does not exist!'"\n"'Change Failed!')
    menu()

def delete_user():
  # Admin Only
  username = input("Username: ")

  if user_exists(username):
    confirm = input("Type 'confirm' to confirm deletion: ")

    if confirm.lower() == "confirm":
      remove_user(username)
      print("Processing. . .  Please Wait!")
      time.sleep(2)
      print(f"User {username} has been removed!")
      menu()

def change_role():
  # Admin Only
  username = input("Username: ")

  if user_exists(username): # <-- checks if the user exists
    new_role = input("New Role: ")
    update_role(username, new_role)
    print("Processing. . .  Please Wait!")
    time.sleep(2)
    print(f"User role for {username} has now been updated to {new_role}")
    menu()

  else:
    print(f'Processing. . . Please Wait!')
    time.sleep(2)
    print(f'User {username} does not exist!'"\n"'Change Failed!')
    menu()
    


def user_exists(username):
  with open("data.txt", "r") as file:
    for line in file:
      userinfo = line.strip().split()
      if username == userinfo[0]:
        return True


def get_user_role(username):
  with open("data.txt", "r") as file:
    for line in file:
      userinfo = line.strip().split(" ")
      if username == userinfo[0]:
        return userinfo[2]

def register_user(username, password, userrole, status, email):
  with open('data.txt', "a") as file:
    file.write(f'{username} {password} {userrole} {status} {email}\n')

def send_email(username, email, code):
  user = 'verifyemailforprogram@gmail.com'
  userpass = 'kfeu oioq uhbl wbjw'

  subject = "Your Verification Code"
  body = f'''
      <html>
          <head>
              <style>
                  body {{
                      font-family: 'Arial', sans-serif;
                      background-color: #f4f4f4;
                      margin: 0;
                      padding: 0;
                      text-align: center;
                  }}
                  .container {{
                      max-width: 600px;
                      margin: 20px auto;
                      background-color: #ffffff;
                      padding: 20px;
                      border-radius: 8px;
                      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                  }}
                  h1 {{
                      color: #333333;
                  }}
                  p {{
                      color: #555555;
                  }}
                  strong {{
                      color: #007bff;
                  }}
              </style>
          </head>
          <body>
              <div class="container">
                  <h1>I come baring a code!</h1>
                  <p>Hey {username}</p>
                  <p> </p>
                  <p>Enter the code below to make sure your actually who you say you are!</p>
                  <p> </p>
                  <p>Your verification code is: <strong>{code}</strong></p>
                  <p> </p>
                  <p>Cheers, The Email Team</p>
                  <p> </p>
                  <p> </p>
                  <p>(If you didn't request this, then these is nothing you can do. Maybe delete this email?)</p>
              </div>
          </body>
      </html>
  '''
  sender = 'verifyemailforprogram@gmail.com'
  receiver = email

  msg = MIMEMultipart()
  msg['From'] = sender
  msg['To'] = receiver
  msg['Subject'] = subject
  msg.attach(MIMEText(body, 'html'))

  with smtplib.SMTP('smtp.gmail.com', 587)as server:
    server.starttls()
    server.login(user, userpass)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)


def generate_code():
  return random.randint(100000, 999999)

def check_password(username, password):
  with open("data.txt", "r") as file:
    for line in file:
      userinfo = line.strip().split(" ")
      if username == userinfo[0] and password == userinfo[1]:
        return True
      

def update_password(username, new_password):
  with open("data.txt", "r") as file:
    lines = file.readlines()

  with open("data.txt", "w") as file:
    for line in lines:
        user_info = line.strip().split(" ")
        if username == user_info[0]:
            file.write(f"{username} {new_password} {user_info[2]} {user_info[3]} {user_info[4]}\n")
        else:
            file.write(line)

def remove_user(username):
  with open("data.txt", "r") as file:
    lines = file.readlines()

  with open("data.txt", "w") as file:
    for line in lines:
        user_info = line.strip().split(" ")
        if username != user_info[0]:
            file.write(line)

def update_email(username, new_email):
  with open("data.txt", "r") as file:
    lines = file.readlines()

  with open("data.txt", "w") as file:
    for line in lines:
      userinfo = line.strip().split(" ")
      if username == userinfo[0]:
        file.write(f"{username} {userinfo[1]} {userinfo[2]} {userinfo[3]} {new_email}\n")
      else:
        file.write(line)

def update_role(username, new_role):
  with open("data.txt", "r") as file:
    lines = file.readlines()

  with open("data.txt", "w") as file:
    for line in lines:
      userinfo = line.strip().split(" ")
      if username == userinfo[0]:
        file.write(f"{username} {userinfo[1]} {new_role} {userinfo[3]} {userinfo[4]}\n")
      else:
        file.write(line)

def get_email(username):
  with open("data.txt", "r") as file:
    for line in file:
      userinfo = line.strip().split(" ")
      if username == userinfo[0]:
        return userinfo[4]

def check_email(username, email):
  with open("data.txt", "r") as file:
    for line in file:
      userinfo = line.strip().split(" ")
      if username == userinfo[0]:
        if email == userinfo[4]:
          return True

def get_user_status(username):
  with open("data.txt", "r") as file:
    for line in file:
      userinfo = line.strip().split(" ")
      if username == userinfo[0]:
        return userinfo[3]


menu()
