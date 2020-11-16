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

# Table format = "student_id | student_pw"
def get_table_name(student_id, student_pw):
    return f'{student_id} | {student_pw}'

def confirm_password():

    while True:
        new_pw = input("Enter password: ")
        new_pw_confirm = input("Confirm password: ")

        if new_pw != new_pw_confirm:
            print("The entered passwords do not match. Please try again\n")
            continue
        break
    
    return new_pw