import os

import MySQLdb
from MySQLdb._exceptions import OperationalError

from helpers import *

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()


def view_tests():
    cursor.execute("USE admin")
    
    tests = []

    cursor.execute("SHOW TABLES")
    for test in cursor.fetchall():
        tests.append(str(test[0]))

    if tests[1:]:
        print(f"{len(tests)} test(s) were found:\n\n {' | '.join(tests)}")
    else:
        print("There are no tests in the database right now")

def view_questions(test_name):
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
    """
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
    """

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

        cursor.execute(f"SELECT MAX(q_no) from {test_name}")
        latest_q_no = cursor.fetchall()[0][0]

        # clean this up, add using lists or something idk
        cursor.execute(f'INSERT INTO {test_name} VALUES ({latest_q_no + 1 if latest_q_no is not None else 1}, {q_type}, {question}, {ques_data.get("weightage", 1)}, {ques_data.get("word_limit", "NULL")}, {" | ".join(ques_data.get("options")) if ques_data.get("options") is not None else "NULL"}, {ques_data.get("answer") if ques_data.get("answer") is not None else "NULL"})')
        db.commit()

        output.append(ques_data)
        
        choice = input("Do you want to add another question to the same test? (y/n): ")
        if choice == "n":
            break

    return output

def remove_question(test_name, question_number):
    # test name will always be valid since its already verified by view_questions
    if cursor.execute(f"DELTE FROM {test_name} WHERE q_no={question_number}") == 0:
        print("Invalid question number")
        return False
    db.commit()

# how do this one
def modify_question(test_name, question_number):
    # will have to take a test property, then check if that property exists
    # maybe make a dict of properties you can edit
    pass
