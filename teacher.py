print("Welcome to the admin panel for JoeMerit\n")

options = {
    1: "View all questions",
    2: "Add a question",
    3: "Remove a question",
    4: "Modify a question"
}

for opt_num in range(1, 5):
    print(f"{opt_num}: {options[opt_num]}")

while True:
    choice = int(input("Please input your choice: "))

    if choice == 1:
        query = "SELECT * FROM questions"
