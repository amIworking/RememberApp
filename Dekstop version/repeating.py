from Library import *
import os
import json
import random
lists = os.listdir('lists')

class Training:
    def __init__(self):
        win = main_win()
        lists = os.listdir('lists')
        label_1 = Main_label(win, "Here are all lists which exist at this moment")
        label_2 = Main_label(win, f"{lists[:]}", 12)
        label_3 = Main_label(win, "Print a name of a list which you wanna train:")
        file_name = tk.Entry(win)
        file_name.pack()
        btn1= BTN(win,lambda:self.file_check(file_name.get(),win),"Searh")
        win.mainloop()

    def file_check(self, note_name, win):
        if note_name+".json" not in os.listdir('lists'):
            message_win(win,f"This list ({note_name}) doesn't exist. Try again")
            return
        else:

            with open(f"lists/{note_name}.json", "r") as r:
                train_list = json.load(r)
            key_words = list(train_list)
            points = 0
            def finishing(win,points):
                message_win(win,f"Your final score is {points} points", "black",True,"normal")
            def file_test(points, old_win,text='',fg="black"):
                if old_win != False:
                    old_win.destroy()
                win = main_win()
                if len(key_words) > 0:
                    ran = random.randrange(len(key_words))
                    label_1 = Main_label(win, f"Translate word '{key_words[ran]}'", 13)
                    answer = tk.Entry(win)
                    label_2 = tk.Label(win, text=text,fg=fg, font=("Arial", 13))
                    answer.pack()
                    label_2.pack()
                    btn2 = BTN(win, lambda: check_answer(answer.get(), points, label_2), "Check")
                    btn3 = BTN(win, lambda: finishing(win,points), "Finish")
                else:
                    message_win(win,f"Your final score is {points} points", "black",True,"normal")
                    return
                def check_answer(answer, points,label_2):
                    print(key_words)
                    if train_list[key_words[ran]] != answer:
                        file_test(points,win,
                                  f"Your answer is wrong\nYour current points:  {points}","red")
                    else:
                        points += 1
                        train_list.pop(key_words[ran])
                        key_words.pop(ran)
                        file_test(points, win,
                                  f"Right!\nYour current points:  {points}", "green")

            file_test(points,False)






"""
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
"""