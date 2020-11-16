import os
import MySQLdb

from helpers_student import *
from options_student import *
from sql_functions_student import *

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()

#table name template = "student_id--student_pw"

cursor.execute("SHOW DATABASES")
if ('students', ) not in cursor.fetchall():
    cursor.execute("CREATE DATABASE students")
    db.commit()

#login/sign_up process
while True:
    cursor.execute("USE students")
    display_options(first_prompt)

    first_choice = get_choice(first_prompt)

    if first_choice == 1:

        while True:
            new_id = input("Enter a test username: ")

            cursor.execute("SHOW TABLES")
            for table_name in cursor.fetchall():
                if table_name.split(" | ")[0] == new_id:
                    print("This username has already been taken. Please choose a different username\n")
                    break
            else:
                break
                
        new_pw = confirm_password()

        # still have to add table columns. Might add datetime to store when their acc/ID was created.
        cursor.execute(f"CREATE TABLE {get_table_name(new_id, new_pw)}")
        print("New ID created")
        logged_in = True

    else:
        login_id = input("Enter your student ID: ")
        login_pw = input("Enter your password: ")

        cursor.execute("SHOW TABLES")
        for table_name in cursor.fetchall():
            if get_table_name(login_id,login_pw) == table_name:
                print("Logged in successfully")
                logged_in = True
        else:
            print("The entered credentials may be wrong or you might not have an account.")
            logged_in = False
    
    if logged_in:
        break

#WIP
while True:
    while True:

        #displaying available tests and getting a test choice for them to attempt
        display_options(get_test_name_dict())
        get_choice(get_test_name_dict())
