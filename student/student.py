import os
import MySQLdb
from textwrap import dedent

from helpers_student import *
from options_student import *
from sql_functions_student import *

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()

#table name template = "student_id | student_pw"

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
            if get_table_name(login_id, login_pw) == table_name:
                print("Logged in successfully")
                logged_in = True
        else:
            print("The entered credentials may be wrong or you might not have an account.")
            logged_in = False
    
    if logged_in:
        break

# WIP
while True:
    while True:

        # displaying available tests and getting a test choice for them to attempt
        test_dict = get_test_name_dict()

        display_options(test_dict)
        choice = get_choice(test_dict)

        cursor.execute("USE admin")
        cursor.execute(f"SELECT * from {test_dict[choice]}")
        questions = cursor.fetchall()

        obj = {"num": 0, "correct": 0}

        for question in questions: # may or may not use while True later to let the student move back and forth b/w questions

            display = f"""
            {question[0]}) {question[2]} [{question[3]}]
            """

            if question[1] == "obj":
                obj["num"] += 1
                display += "\n\n"

                for count, option in enumerate(question[5].split(" | "), start = 1):
                    display += f"{count}. {option}\n"

            else:
                if question[4] is not None:
                    display += f"Word limit: {question[4]} words\n"
            
            print(dedent(display))

            while True:
                answer = input("\nYour answer: ")

                if question[1] == "obj":

                    if not answer.isdigit():
                        print("Please enter the option number to answer an objective type question")
                        continue
                    
                    if int(answer) not in range(1, 5):
                        print("Invalid option")
                        continue
                
                else:
                    if question[4] is not None:
                        if len(answer.split()) > question[4]:
                            print(f"Your answer is {len(answer)} words long, please keep it under the word limit of {question[4]} words")
                            continue
                break

            if question[1] == "obj":
                if int(answer) == int(question[6]):
                    obj["correct"] += 1
            
            # add answer to answers db or table or whatever one by one
        
        display = "The test is now over"
        if obj["num"]:
            display += f". Your objective score was {obj['correct']}/{obj['num']}"
        
        print(display)
