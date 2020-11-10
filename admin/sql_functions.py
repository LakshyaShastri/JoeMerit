import os

import MySQLdb
from MySQLdb._exceptions import OperationalError

from helpers import *

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()


def view_tests():
    try:
        cursor.execute("USE admin")
    except OperationalError:
        print("There are no tests in the database as of now")
    
    tests = []

    cursor.execute("SHOW TABLES")
    for test in cursor.fetchall():
        tests.append(str(test[0]))
    
    print(f"{len(tests)} test(s) were found:\n\n {' | '.join(tests)}")

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

    cursor.execute(f"SELECT * FROM {test_name}") # needs to be changed to show just questions
    for row in cursor.fetchall():
        print(row) # same as above, display as:
    
    # subject to change, display everything neatly in command line

    # if subj:
    #     Question number:
    #     Question weightage:
    #     Question word limit:
    #     Question: 
    # else:
    #     Question number:
    #     Question:
    #     Question options:
    #     Answer:


def add_questions(test_name):
    '''
    output_structure = [
        {
            "type": str,
            "question": str,
            "weightage": Optional[int],
            "word_limit": Optional[int],
            "options": [
                str, str, str, str
            ],
            "answer": int,
        }
    ]
    '''

    output = []

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
        
        ques_data = {}
        ques_data["type"] = q_type
        ques_data["question"] = question

        if q_type == 'subj':
            weightage = int(input("Enter the marks the question should carry: "))
            word_limit = int(input("Enter an optional word limit for the question (leave blank for no word limit): "))

            if word_limit in {"", " "}:
                word_limit = None
            
            ques_data["weightage"] = weightage
            ques_data["word_limit"] = word_limit

        else:
            options = {}
            for option_num in range(1, 5):
                options[option_num] = input(f"Enter option number {option_num}")
            
            display_options(options)
            answer = int(input(f"Which option is the answer to the question? "))

            ques_data["options"] = list(options.values())
            ques_data["answer"] = answer

        # clean this up, add using lists or something idk
        cursor.execute(f'INSERT INTO {test_name} VALUES ({q_type}, {question}, {ques_data.get("weightage", 1)}, {ques_data.get("word_limit", "NULL")}, {" | ".join(ques_data.get("options")) if ques_data.get("options") is not None else "NULL"}, {ques_data.get("answer") if ques_data.get("answer") is not None else "NULL"})')

        output.append(ques_data)
        
        choice = input("Do you want to add another question to the same test? (y/n): ")
        if choice == "n":
            break

    return output

def remove_question(test_name, question_number):
    # check if question number exists in test_name
    # test name will always be valid since its already verified by view_questions
    pass

# how do this one
def modify_question(test_name, question_number):
    # will have to take a test property, then check if that property exists
    # maybe make a dict of properties you can edit
    pass
