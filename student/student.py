import os
import MySQLdb


from student.helpers_student import *
from student.options_student import *
from student.sql_functions_student import qwe



db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()




#table name template = "student_id--student_pw"



qwe("SHOW DATABASES")
if ('students', ) not in cursor.fetchall():
    qwe("CREATE DATABASE students")
    db.commit()





while True:

    qwe("USE students")
    #login/sign-up?
    display_options(first_prompt)
    first_choice = get_choice(first_prompt)

    while True:


        #sign-up
        if first_choice == 1:


            new_id = input("Enter a unique username: ")
            qwe("SHOW TABLES")
            for table_name in cursor.fetchall():
                if table_name.split("--")[0] == new_id:
                    print("This username has already been taken. Please choose a different username.")
                    break


            new_pw = input("Enter password: ")
            new_pw_confirm = input("Confirm password: ")


            if "-" in new_pw or "-" in new_id:
                print("Your ID/password should not contain a hyphen (-). Please try again.")
                break
            if new_pw != new_pw_confirm:
                print("The entered passwords do not match. Please try again.")
                break
            break
        

        #login
        elif first_choice == 2:


            login_id = input("Enter your student ID: ")
            login_pw = input("Enter your password: ")

            qwe("SHOW TABLES")
            for table_name in cursor.fetchall():

                if get_table_name(login_id,login_pw) == table_name:
                    print("Logged in successfully.")
                    break
                
                else:
                    print("The entered credentials may be wrong. Please try again.")
                break    
            break
        break



