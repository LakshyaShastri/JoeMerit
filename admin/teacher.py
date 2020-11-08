import os

import MySQLdb

from admin.options import *
from admin.helpers import *

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()

print("Welcome to the admin panel for JoeMerit\nPlease choose an option:\n")

def view_questions():
    query = "SELECT * FROM questions"
    # execute, whatever the db name or format is

def add_questions(test_name):
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

while True:
    display_options(main_options)
    choice = get_choice(main_options)

    if choice == 1:
        test_name = input("Enter the name of the test/subject: ")
        # add test name to table of tests; create table for the test
        add_questions(test_name)

    elif choice == 2:

        while True:
            display_options(view_options)
            subchoice = get_choice(view_options)

            if subchoice == 1:
                pass
            elif subchoice == 2:
                pass
            elif subchoice == 3:
                pass
            elif subchoice == 4:
                pass
            elif subchoice == 5:
                break


    elif choice == 3:
        pass
