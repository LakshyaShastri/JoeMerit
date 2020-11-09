import os
import MySQLdb
from MySQLdb._exceptions import ProgrammingError
from admin.options import *
from admin.helpers import *
from time import sleep


db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()

print("Welcome to the admin panel for JoeMerit\nPlease choose an option:\n")



def view_questions(test_name):
    # check if test_name exists or not

    cursor.execute("USE ADMIN")
    cursor.execute(f"SELECT * FROM {test_name}")
    
    for row in cursor.fetchall():
        print(row)

def add_question(test_name):
    # check if a table called test_name exists or not
    if test_name not in cursor.fetchall():
        print("{test_name} was not found.")
        return False    

    while True:

        while True:
            q_type = input("Do you want to enter a subjective question or an objective question? (subj/obj): ")
            if q_type not in {'subj', 'obj'}:
                print("Invalid input")
                continue
            break
        
        question = input("Enter the question: ")

        if q_type == 'subj':
            weightage = int(input("Enter the marks the question should carry: "))
            word_limit = int(input("Enter an optional word limit for the question (leave blank for no word limit): "))

            if word_limit in {"", " "}:
                word_limit = None
            
            # add question, weightage and word limit (if any) to the db of test_name
            # add NULL if no word limit

        else:
            options = {}
            for option_num in range(1, 5):
                options[option_num] = input(f"Enter option number {option_num}")
            
            display_options(options)
            answer = int(input(f"Which option is the answer to the question? "))

            # add question, answer and options to db of test_name

def remove_question(test_name, question_number):
    # check if question number exists in test_name
    # test name will always be valid since its already verified by view_questions
    pass

# how do this one
def modify_question(test_name, question_number):
    # will have to take a test property, then check if that property exists
    # maybe make a dict of properties you can edit
    pass





#INSERT INTO TABLE VALUES (/TES, DFB,S GU)


#making DB and master_table
try:
    cursor.execute("CREATE DATABASE ADMIN;")
    cursor.execute("USE ADMIN;")
    cursor.execute("CREATE TABLE MASTER (test_name CHAR(20), num_ques DECIMAL(3), subj_ques DECIMAL(3), obj_ques DECIMAL(3), max_marks DECIMAL(3), test_date DATE;")
except ProgrammingError:
    print("You are already using the ADMIN database. The master table has already been created.")
    sleep(2)
    print("Loading options...")
    sleep(2)



while True:
    display_options(main_options)
    choice = get_choice(main_options)

    if choice == 1:
        test_name = input("Enter the name of the test: ")
        # add test name to table of tests; create table for the test
        
        add_question(test_name)

    elif choice == 2:

        while True:
            display_options(view_options)
            subchoice = get_choice(view_options)

            if subchoice == 1:
                view_questions()
            elif subchoice == 2:
                test_name = input("Enter the test name you want to add a question to: ")
                add_question(test_name)

            elif subchoice == 3:
                test_name = input("Enter the test name you want to remove a question from")
                view_questions(test_name)
                question_number = int(input("Enter the question number you want to remove: "))
                remove_question(test_name, question_number)

            elif subchoice == 4:
                modify_question()

            elif subchoice == 5:
                break


    elif choice == 3:
        pass
