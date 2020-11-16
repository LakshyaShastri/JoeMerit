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

def interpret_output(output):
    total_ques = len(output)
    subj_ques_num = len([ques for ques in output if ques['type'] == "subj"])
    obj_ques_num = len([ques for ques in output if ques['type'] == "obj"])
    max_marks = sum([ques.get('weightage') if ques.get('weightage') is not None else 1 for ques in output])

    return {
        "total_ques": total_ques,
        "subj_ques_num": subj_ques_num,
        "obj_ques_num": obj_ques_num,
        "max_marks": max_marks
    }
