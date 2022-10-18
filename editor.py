import os
import json
lists = os.listdir('lists')
def deleting():
    while True:
        print("Here are all lists which exist at this moment")
        print(lists)
        note_name = input("Print a name of a list which you wanna delete:\n")
        if note_name + ".json" not in lists:
            print("This list doesn't exist. Try again")
            continue
        else:
            print("Are you sure about deleting the list?")
            answer = input("Print 'yes' if you are sure"
                  "or press any other symbols if you aren't")
            if answer.lower() == 'yes':
                os.rmdir(f"lists/{note_name}"+'.json')
                print("Deleting was successfull")

def edition():
    while True:
        print("Here are all lists which exist at this moment")
        print(lists)
        note_name = input("Print a name of a list which you wanna edit:\n")
        if note_name == 'q':
            return
        if note_name + ".json" not in lists:
            print("This list doesn't exist. Try again")
            continue
        else:
            with open(f"lists/{note_name}.json", "r") as r:
                edit_list = json.load(r)
            print("Which word of the list you'd want to edit\n"
                  f"Pick a word from 1 to {len(edit_list)}")
            num_str = ''
            for i in range(1, len(edit_list) + 1):
                num_str += str(i)
            n = 0
            for key, value in edit_list.items():
                n+=1
                print(f"{n}.{key} - {value} ", end='')
            print()
            keys_list = list(edit_list)
            word_num = input()
            if word_num not in num_str:
                print('Your wrote a wrong number')
            else:
                edit_word = keys_list[int(word_num)-1]
                print(f"You chose this word: '{edit_word}'.\n")
                while True:
                    print("Print your target word and the translation and paste 'space' between them")
                    new_string = input()
                    if " " not in new_string or new_string.count(" ") > 1:
                        print("You have to add '' between words and can't more than 1 space")
                        continue
                    new_word = new_string.split(" ")
                    if new_word[0] in edit_list:
                        print("This word already exists")
                        continue
                    else:
                        print(edit_word, edit_list)
                        print(f"You changed {edit_word} - {edit_list[edit_word]}"
                              f"to {new_word[0]} - {new_word[1]}")
                        edit_list[new_word[0]] = new_word[1]
                        edit_list.pop(edit_word)
                        print("Your list has been successfully saved")
                        with open(f"lists/{note_name}.json", "w") as f:
                            json.dump(edit_list, f)
                        print("if you wanna quiet, print 'q'")
                        break
