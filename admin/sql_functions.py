import os

import MySQLdb
from MySQLdb._exceptions import OperationalError

from helpers import *
from options import test_table_properties

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()


def view_tests():
    cursor.execute("USE admin")
    
    tests = []

    cursor.execute("SHOW TABLES")
    for test in cursor.fetchall():
        tests.append(str(test[0]))

    tests.pop(0) # popping the master table
    if tests:
        print(f"{len(tests)} test(s) were found:\n\n {' | '.join(tests)}")
    else:
        print("There are no tests in the database right now\n")

def view_questions(test_name):
    cursor.execute("USE admin")
    
    cursor.execute("SHOW TABLES")
    if (test_name, ) not in cursor.fetchall():
        print(f"A test called {test_name} does not exist\n")
        return False

    cursor.execute(f"SELECT * FROM {test_name}")
    questions = cursor.fetchall()

    for question in questions:

        ques_print = f"""
            {question[0]}) {question[2]}

            Question weightage: {question[3]}\n
        """

        if question[1] == "subj":
            ques_print += f"Question word limit: {question[4] if question[4] is not None else 'No word limit specified'}"

        else:
            ques_print+="\n"
            options = question[5].split(" | ")

            for index, option in enumerate(options, start=1):
                ques_print += f"{index}) {option}\n"

            ques_print += f"Answer: {question[6]}"

        print(ques_print)

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
            word_limit = input("Enter an optional word limit for the question (leave blank for no word limit): ")

            if word_limit in {"", " "}:
                word_limit = None
            else:
                word_limit = int(word_limit)
            
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
    if cursor.execute(f"DELETE FROM {test_name} WHERE q_no={question_number}") == 0:
        print("Invalid question number")
        return False
    db.commit()






def modify_question(test_name, question_number):

    while True:

        display_options(test_table_properties)
        operation = get_choice(test_table_properties)

    
        if operation == 1:
            new_ques = input("Enter new question: ")
            cursor.execute(f"UPDATE {test_name} SET question = '{new_ques}' WHERE q_no = {question_number}")
        
            print("The mentioned change has been made.")
            break


        elif operation == 2:
            new_weig = input("Enter new weightage: ") 
            cursor.execute(f"UPDATE {test_name} SET weightage = {new_weig} WHERE q_no = {question_number}")
            break

        elif operation == 3:
            try:
                cursor.execute(f"SELECT type FROM {test_name} WHERE q_no = {question_number} AND type = 'subj';")
                new_word_limit = input("Enter new word limit: ")
                cursor.execute(f"UPDATE {test_name} SET word_limit = '{new_word_limit}' WHERE q_no = {question_number}")
                break
            except:
                print("Cannot modify word limit of an obj type question.")
                continue
        
        elif operation == 4:
            try:
                cursor.execute(f"SELECT type FROM {test_name} WHERE q_no = {question_number} AND type = 'obj';")
                #displaying options
                for choice in range(0,4):
                    print(test_table_properties[4][choice])

                while True:

                    #displaying options
                    for choice in range(0,4):
                        print(test_table_properties[4][choice])

                    change_choice = int(input("Choose an option to edit: "))
                    change = input("Enter new option: ")
                    test_table_properties[4][change_choice] = change

                    cursor.execute(f"UPDATE {test_name} SET options = {test_table_properties[4]} WHERE q_no={question_number};")
                    loop_gov = input("Changes made. Do you want to make further changes?(y/n)")
                    if loop_gov.lower() == "n":
                        break

            except:
                print("Cannot modify word limit of an obj type question.")

        
        elif operation == 5:
            #displaying option containing dict
            print(test_table_properties[4])
            answer_input = int(input("Which of the following should be considered as the answer for the given question?"))
            if answer_input in {1,2,3,4}:
                #The options will be contained in a list. The answer is being stored as a string.
                cursor.execute(f"UPDATE {test_name} SET answer = {test_table_properties[4][answer_input - 1]} WHERE q_no = {question_number};")

    


    db.commit()






def delete_test(test_name):
    del_confirm = input(f"Are you sure you want to delete test {test_name} permanently? (y/n): ")
    
    if del_confirm.lower() == "n":
        return False

    cursor.execute("USE admin")
    cursor.execute(f"DROP TABLE {test_name}")
    cursor.execute(f"DELETE FROM master WHERE test_name={test_name}")
    db.commit()

    print(f"Table {test_name} has been successfully deleted.")
