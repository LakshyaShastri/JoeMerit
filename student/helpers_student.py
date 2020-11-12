import MySQLdb


def get_choice(options_dict):
    while True:
        choice = int(input("Please enter your choice: "))
        print()

        if choice not in options_dict:
            print("Invalid choice\n")
            continue

        return choice



def display_options(option_dict):
    for opt_num in option_dict:
        print(f"{opt_num}: {option_dict[opt_num]}")




#table name = "student_id--student_pw"
def get_table_name(student_id,student_pw):
    name = (f'{student_id}--{student_pw}')
    return name