import os
import json
import random
lists = os.listdir('lists')
def training():
    while True:
        print("Here are all lists which exist at this moment")
        print(lists)
        note_name = input("Print a name of a list which you wanna train:\n")
        if note_name.lower() == 'q':
            return
        if note_name+".json" not in lists:
            print("This list doesn't exist. Try again")
            continue
        with open(f"lists/{note_name}.json", "r") as r:
            train_list = json.load(r)
        key_words = list(train_list)
        points = 0
        while True:
            print(train_list)
            print(key_words)
            if len(key_words)>0:
                ran = random.randrange(len(key_words))
                print(f"Translate word '{key_words[ran]}'")
                answer = input()
                if train_list[key_words[ran]] != answer:
                    print("Your answer is wrong")
                    print("Your current points: ", points)
                    continue
                else:
                    points+=1
                    print("Right")
                    print("Your current points: ", points)
                    train_list.pop(key_words[ran])
                    key_words.pop(ran)
                    continue
            else:
                print(f"Your final score is {points} points")
                print("if you wanna quiet, print 'q'")
                break
