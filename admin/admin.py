import os
from datetime import datetime

import MySQLdb

from options import *
from helpers import *
from sql_functions import *

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()


cursor.execute("SHOW DATABASES")
if ('admin', ) not in cursor.fetchall():
    cursor.execute("CREATE DATABASE ADMIN;")

cursor.execute("USE admin")

cursor.execute("SHOW TABLES")
if ('MASTER', ) not in cursor.fetchall():
    cursor.execute("CREATE TABLE master (test_name VARCHAR(20), subj_ques DECIMAL(2,0), obj_ques DECIMAL(2,0), num_ques DECIMAL(2,0), max_marks DECIMAL(3,1), created_at TIMESTAMP;")


print("Welcome to the admin panel for JoeMerit\nPlease choose an option:\n")
while True:
    display_options(main_options)
    choice = get_choice(main_options)

    if choice == 1:
        test_name = input("Enter the name of the test: ")
        test_name.replace(" ", "_")

        cursor.execute("USE admin")
        cursor.execute("SHOW TABLES")

        if (test_name, ) in cursor.fetchall():
            print(f"A test named {test_name} already exists")
            continue
        
        cursor.execute(f"CREATE TABLE {test_name} (q_no DECIMAL(2), type VARCHAR(4), question VARCHAR(120), weightage DECIMAL(1), word_limit DECIMAL(3), options VARCHAR(300), answer DECIMAL(1);")
        db.commit()

        data = interpret_output(add_questions(test_name))

        cursor.execute(f"INSERT INTO master VALUES ({test_name}, {data['subj_ques_num']}, {data['obj_ques_num']}, {data['subj_ques_num'] + data['obj_ques_num']}, {datetime.now().timestamp()})")
        db.commit()

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
                add_questions(test_name)

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
