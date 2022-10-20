import json
import os
new_list = {}
def writing_json(file_name, data):
    with open(f"lists/{file_name}.json","w") as f:
        json.dump(data, f)
def creation_new_list():
    print(os.listdir("lists"))
    while True:
        print("Come up with a new name for your new list:")
        note_name = input()
        if len(note_name)<1:
            print("Your name has to contain at least 1 symbol")
        elif note_name+'.json' in os.listdir("lists"):
            print("This name already exists")
        else:
            print("Your file has been successfully saved")
            break
    writing_json(note_name, {})
    return note_name


def filling_new_list():
    note_name = creation_new_list()
    print("How many words do you wanna add?")
    amountOfWords = int(input())
    exit_flag = False
    for i in range(amountOfWords):
        if exit_flag == True:
            writing_json(note_name, new_list)
            print("Your list has been successfully saved")
            break
        while True:
            print("Print your target word and the translation and paste 'space' between them")
            print(f"Print your {i + 1} word")
            new_string = input()
            if new_string.lower() == 's':
                exit_flag = True
                break
            if " " not in new_string or new_string.count(" ") > 1:
                print("You have to add '' between words and can't more than 1 space")
                continue
            new_word = new_string.split(" ")
            if new_word[0] in new_list:
                print("This word already exists")
                continue
            else:
                new_list[new_word[0]] = new_word[1]
                break
    print(new_list)
    writing_json(note_name, new_list)
    print("Your list has been successfully saved")
    input()
    return

