from Library import *
import json
import os
import tkinter as tk
import math
import  time
from functools import partial
new_list = {}
min_width = 700

class List_maker:
    def __init__(self):
        win = main_win()
        label_1 = tk.Label(win, text="Come up with a new name for your new list: ",
                           bg="#dbdbdb", font=("Arial", 15),
                           padx=20, pady=20, width=min_width)
        label_1.pack()
        file_name = tk.Entry(win)
        file_name.pack()
        btn1 = tk.Button(win, text='Save1',
                         command=lambda:self.checking_lists_name(file_name.get(),win),
                         bg="#dbdbdb", font=("Arial", 14),
                         padx=20, pady=5, )
        btn1.pack()
        win.mainloop()
    def writing_json(self,file_name, data):
        with open(f"lists/{file_name}.json", "w") as f:
            json.dump(data, f)

    def checking_lists_name(self, note_name, win):
        print(note_name)
        if len(note_name) < 1:
            print("Your name has to contain at least 1 symbol")
            message_win(win, "Your name has to contain at least 1 symbol")
        elif note_name + '.json' in os.listdir("lists"):
            message_win(win, "This name already exists",)
        else:
            message_win(win, "Your file has been successfully saved", True, "black")
            self.amountOfWords(note_name)
            #self.writing_json(note_name, {})


    def amountOfWords(self, note_name):
        win = main_win()
        label_1 = tk.Label(win, text="How many words do you wanna add?",
                           bg="#dbdbdb", font=("Arial", 15),
                           padx=20, pady=20, width=300)
        label_1.pack()
        amount = tk.Entry(win)
        amount.pack()
        print(amount.get())
        btn1 = tk.Button(win, text='Save2',
                         command=lambda: self.filling_new_list(win,amount.get(), note_name),
                         bg="#dbdbdb", font=("Arial", 14),
                         padx=20, pady=5, )
        btn1.pack()
        win.mainloop()

        print("OK")
    def filling_new_list(self, win, amountOfWords, note_name):
        print(amountOfWords, type(amountOfWords))
        try:
            amountOfWords = int(amountOfWords)
        except ValueError:
                message_win(win,"You didn't write a num")
        else:
            win.destroy()
            win = main_win()
            label_1 = tk.Label(win, text="Fill all fields",
                               bg="#dbdbdb", font=("Arial", 15),
                               padx=20, pady=20)
            label_1.grid(row=0)
            fields = []
            words = []
            for i in range(1,amountOfWords+1):
                for j in range(2):
                    field = tk.Entry(win)
                    field.grid(row=i, column=j)
                    fields.append(field)
            btn3 = tk.Button(win, text='Save3',
                             command=lambda: self.list_saving(win,fields, note_name),
                             bg="#dbdbdb", font=("Arial", 14),
                             padx=20, pady=5, )
            btn3.grid(row=amountOfWords+3, column=0)
            win.mainloop()
    def list_saving(self, win,fields, note_name):
        words = []
        print(note_name, "here")
        for i in range(len(fields)):
            if fields[i].get()=='':
                message_win(win,"You have at least 1 empty field")
                break
            elif i!=len(fields)-1 and i%2==0:
                words.append([fields[i].get(),fields[i+1].get()])
        new_dict = {}
        for i in words:
            new_dict[i[0]]=i[1]
        # self.writing_json(note_name, {})
        print("Ok")







"""
def filling_new_list():
    note_name = creation_new_list()
    print("How many words do you wanna add?")
    amountOfWords = int(input())
    exit_flag = False
    for i in range(amountOfWords):
        if exit_flag == True:
            #writing_json(note_name, new_list)
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
    #writing_json(note_name, new_list)
    print("Your list has been successfully saved")
    return
"""