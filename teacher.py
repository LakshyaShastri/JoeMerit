print("Welcome to the admin panel for JoeMerit\nPlease choose an option:\n")

main_options = {
    1: "Create a test",
    2: "View/edit a test",
    3: "Delete a test"
}

def get_choice():
    choice = int(input("Please enter your choice: "))
    print()
    return choice

def view_questions():
    query = "SELECT * FROM questions"

while True:
    for opt_num in main_options:
        print(f"{opt_num}: {main_options[opt_num]}")

    choice = get_choice()
    if choice not in main_options:
        print("Invalid choice\n")
        continue

    if choice == 1:
        pass


    elif choice == 2:
        options = {
            1: "View all questions",
            2: "Add a question",
            3: "Remove a question",
            4: "Modify a question",
            5: "Go back"
        }

        while True:
            for opt_num in options:
                print(f"{opt_num}: {options[opt_num]}")
            
            subchoice = get_choice()
            if subchoice not in options:
                print("Invalid choice\n")
                continue

            if subchoice == 1:
                view_questions()
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
