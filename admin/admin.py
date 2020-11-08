from options import *
from helpers import *
from sql_functions import *

print("Welcome to the admin panel for JoeMerit\nPlease choose an option:\n")

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
