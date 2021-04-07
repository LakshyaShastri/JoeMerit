import os
import ast
import MySQLdb
from textwrap import dedent
from datetime import datetime

from student.helpers_student import *
from student.options_student import *
from student.sql_functions_student import *

from admin.options_admin import *
from admin.helpers_admin import *
from admin.sql_functions_admin import *

while True:
    person = input("Do you want to continue as a teacher, a student or exit the program? (t/s/e): ")
    if person.lower() not in {'t', 's', 'e'}:
        print("Invalid input, please try again\n")
        continue

    if person == 's':
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
                    login_id = input("Enter a username: ")

                    cursor.execute("SHOW TABLES")
                    for table_name in cursor.fetchall():
                        if table_name.split(" | ")[0] == login_id:
                            print("This username has already been taken. Please choose a different username\n")
                            break
                    else:
                        break
                        
                login_pw = confirm_password()

                # still have to add table columns. Might add datetime to store when their acc/ID was created.
                cursor.execute(f"CREATE TABLE {get_table_name(login_id, login_pw)} (test_name VARCHAR(20), subj_ans VARCHAR(1000), obj_ans DECIMAL(1),  subj_score DECIMAL(3), obj_score DECIMAL(3)")
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



        #Logged in, starting test choosing, attempting and result viewing process
        while True:
            
            display_options(second_prompt)

            prompt_choice = get_choice(second_prompt)

            if prompt_choice == 1:

                while True:

                    # displaying available tests and getting a test choice for them to attempt
                    test_dict = get_test_name_dict()

                    display_options(test_dict)
                    choice = get_choice(test_dict)

                    cursor.execute("USE admin")
                    cursor.execute(f"SELECT * from {test_dict[choice]}")
                    questions = cursor.fetchall()

                    obj = {"num": 0, "correct": 0}
                    subj = {}

                    #q_no: answer_chosen
                    obj_ans = {}

                    for question in questions: # may or may not use while True later to let the student move back and forth b/w questions
                        """
                        question
                        0 = question number
                        1 = type
                        2 = question
                        3 = weightage
                        4 = word limit
                        5 = options
                        6 = answer
                        """

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
                                if " | " in answer:
                                    print('Your answer cannot contain " | " in it.')
                                    continue

                                if question[4] is not None:
                                    if len(answer.split()) > question[4]:
                                        print(f"Your answer is {len(answer)} words long, please keep it under the word limit of {question[4]} words")
                                        continue

                                subj[question[0]] = answer

                            break

                        if question[1] == "obj":
                            obj_ans[question[0]] = answer

                            if int(answer) == int(question[6]):
                                obj["correct"] += 1

                    display = "The test is now over"
                    if obj["num"]:
                        display += f". Your objective score was {obj['correct']}/{obj['num']}"

                    print(display)

                    cursor.execute("USE student")
                    cursor.execute(f'INSERT INTO {get_table_name(login_id, login_pw)} VALUES ({test_dict[choice]}, {str(subj)}, {str(obj_ans)}, "NULL", {str(obj)})')

            elif prompt_choice == 2:

                while True:

                    while True:
                        if not logged_in:
                            print("Please log in:")
                            login_id = input("Enter your student ID: ")
                            login_pw = input("Enter your password: ")

                            cursor.execute("SHOW TABLES")
                            for table_name in cursor.fetchall():
                                if get_table_name(login_id, login_pw) == table_name:
                                    print("Logged in successfully")
                                    logged_in = True
                                    break
                            else:
                                print("The entered credentials may be wrong or you might not have an account.")
                                logged_in = False
                        else:
                            break

                    if logged_in:
                        cursor.execute('USE students')
                        tests = get_test_name_dict()
                        display_options(tests)

                        test_name = get_choice(tests)

                        cursor.execute(f'SELECT obj_score, subj_score FROM {get_table_name(login_id, login_pw)} WHERE test_name = {test_name}')

                        score_data = cursor.fetchall()

                        if (score_data[0] == 'NULL') and (score_data[1]) == 'NULL':
                            print('There is no data for you corresponding to this test. Please confirm if you have attempted this test successfully')

                        elif score_data[0] == 'NULL':
                            print(f'Your subjective score for this test is {score_data[1]}')

                        elif score_data[1] == 'NULL':
                            print(f'Your objective score for this test is {score_data[0]}')

                        else:
                            print(f'Your objective score for this test: {score_data[0]}')
                            print(f'Your subjective score for this test: {score_data[1]}')

                        break
            
            elif prompt_choice == 3:
                print("Exiting program")
                break
        
    elif person == 't':
        db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
        cursor = db.cursor()

        cursor.execute("SHOW DATABASES")
        if ('admin', ) not in cursor.fetchall():
            cursor.execute("CREATE DATABASE admin")
            db.commit()

        cursor.execute("USE admin")

        cursor.execute("SHOW TABLES")
        if ('master', ) not in cursor.fetchall():
            cursor.execute("CREATE TABLE master (test_name VARCHAR(20), subj_ques DECIMAL(2,0), obj_ques DECIMAL(2,0), num_ques DECIMAL(2,0), max_marks DECIMAL(3,1), created_at TIMESTAMP)")
            db.commit()


        print("\nWelcome to the admin panel for JoeMerit\nPlease choose an option:\n")
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
                
                cursor.execute(f"CREATE TABLE {test_name} (q_no DECIMAL(2), type VARCHAR(4), question VARCHAR(120), weightage DECIMAL(1), word_limit DECIMAL(3), options VARCHAR(300), answer DECIMAL(1))")

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
                        testName = input('Enter name of test whose properties are to be modified: ')
                        ques_no = input('Enter question number to be edited: ')
                        modify_question(testName, ques_no)

                    elif subchoice == 6:
                        break

            elif choice == 3:
                    
                test_name = input("Enter the test name which you want to delete: ")

                cursor.execute("SHOW TABLES")
                if (test_name, ) not in cursor.fetchall():
                    print(f"A test called {test_name} does not exist")
                    
                else:
                    delete_test(test_name)

            elif choice == 4:
                while True:

                    while True:

                        test_name = input("Enter the exact test name for which you want to grade the class: ")
                        cursor.execute("USE admin")
                        cursor.execute("SHOW TABLES")


                        if (test_name ,) in cursor.fetchall():
                            print("This test does not exist or is invalid. Please enter the correct test name.")
                            break
                        
                        cursor.execute("USE students")
                        cursor.execute("SHOW TABLES")
                        
                        for student in cursor.fetchall():
                    
                            student_name = student[0][0].split(" | ")



                            print(f"Grading test for {student_name}.")
                            cursor.execute(f"SELECT * FROM {student} WHERE test_name = {str(test_name)}")
                            horizontal = cursor.fetchone()
                            all_answers = horizontal[0][1]

                    
                            #question extraction

                            cursor.execute("USE admin")

                            cursor.execute(f"SELECT question FROM {test_name} WHERE type = 'subj'")
                            all_questions = cursor.fetchall()
                            cursor.execute(f"SELECT weightage FROM {test_name} WHERE type = 'subj'")
                            all_weightages = cursor.fetchall()

                            score_dict = {}

                            #single question-answer extraction and display
                            for i in range(0,(len(all_questions)[0]+1)):

                                print(f"Question:\n{all_questions[i]}")

                                print(f"Given answer:\n{all_answers[i]}")

                                print(f"weightage: {all_weightages[i]}")

                                while True:

                                    score = input("Enter score: ")

                                    if score.isalpha():
                                        print("The score should be an integer. Try again.")
                                        continue
                            
                                    if int(score) > int(all_weightages[i]):
                                        print("The score cannot be more than the weightage. Try again.")
                                        continue

                                    score_dict[i] = score

                                    break


                            cursor.execute("USE students")
                            #make a dict to store the respective scores

                            cursor.execute(f"UPDATE {student} SET sub_score = {str(score_dict)} WHERE test_name = {test_name}")
                        
                        print("You have marked all answers.")
                        break
                    break





            elif choice == 5:


                while True:

                    test_name = input("Enter test name for which results are to be viewed: ")
                    
                    #checking if the test exists
                    cursor.execute("USE admin")
                    cursor.execute("SHOW TABLES")
                    if (test_name, ) not in cursor.fetchall():
                        print("The entered test name does not exist. Please enter a valid test.")
                        break

                            

                    cursor.execute("USE students")       
                    cursor.execute("SHOW TABLES")

                    all_tables = cursor.fetchall()            

                    for user in all_tables:
                    #getting total score for one student and displaying it
                        #initializing da ting
                        cursor.execute(f"SELECT subj_score FROM {(user ,)[0]} WHERE test_name = {test_name}")
                        scores = dict(cursor.fetchall()[0])

                        total_score = get_total_score(scores)
                        
                        student_username = user[0][0].split(" | ")[0]

                        #displaying da ting
                        print(f"Subjective score for {student_username} : {total_score}\n")
                        
                    cont = input("Do you want to conitnue for other tests? (y/n)")

                    if cont.lower() == "y":
                        continue

                    elif cont.lower() == "n":
                        break

    else:
        print("Exiting program. . .")
        break
