import os

import MySQLdb

from options import *
from helpers import *

db = MySQLdb.connect(host = "localhost", user = "root", passwd = os.environ['sqlpwd'])
cursor = db.cursor()

print("Welcome to the admin panel for JoeMerit\nPlease choose an option:\n")

def view_questions():
    query = "SELECT * FROM questions"

while True:
    display_options(main_options)
    choice = get_choice(main_options)

    if choice == 1:
        subject_name = input("Enter the name of the subject: ")

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
