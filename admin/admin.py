import os

import MySQLdb
from MySQLdb._exceptions import OperationalError

from options import *
from helpers import *

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()

print("Welcome to the admin panel for JoeMerit\nPlease choose an option:\n")

def view_tests():
    try:
        cursor.execute("USE admin")
    except OperationalError:
        print("There are no tests in the database as of now")
    
    cursor.execute("SHOW TABLES")
    for test in cursor.fetchall():
        print(test[0])

def view_questions(test_name):
    try:
        cursor.execute("USE admin")
    except OperationalError:
        cursor.execute("CREATE DATABASE admin")
        cursor.execute("USE admin")
    
    cursor.execute("SHOW TABLES")
    if (test_name, ) not in cursor.fetchall():
        print(f"A test called {test_name} does not exist\n")
        return False

    cursor.execute(f"SELECT * FROM {test_name}")
    for row in cursor.fetchall():
        print(row)

def add_question(test_name):
    cursor.execute("USE admin")
    cursor.execute("SHOW TABLES")

    if (test_name, ) not in cursor.fetchall():
        print(f"A test called {test_name} does not exist\n")
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
        
        # cursor.execute("")
        
        choice = input("Do you want to add another question to the same test? (y/n): ")
        if choice == "n":
            break

def remove_question(test_name, question_number):
    # check if question number exists in test_name
    # test name will always be valid since its already verified by view_questions
    pass

# how do this one
def modify_question(test_name, question_number):
    # will have to take a test property, then check if that property exists
    # maybe make a dict of properties you can edit
    pass

while True:
    display_options(main_options)
    choice = get_choice(main_options)

    if choice == 1:
        test_name = input("Enter the name of the test/subject: ")
        # add test name to table of tests; create table for the test
        add_question(test_name)

    elif choice == 2:

        while True:
            display_options(view_options)
            subchoice = get_choice(view_options)


            if subchoice == 1:
                view_tests()
            elif subchoice == 2:
                test_name = input("Enter the test name you want to see the questions of: ")
                view_questions(test_name)
            elif subchoice == 3:
                test_name = input("Enter the test name you want to add a question to: ")
                add_question(test_name)

            elif subchoice == 4:
                test_name = input("Enter the test name you want to remove a question from")
                view_questions(test_name)
                question_number = int(input("Enter the question number you want to remove: "))
                remove_question(test_name, question_number)

            elif subchoice == 5:
                modify_question()

            elif subchoice == 6:
                break


    elif choice == 3:
        pass
