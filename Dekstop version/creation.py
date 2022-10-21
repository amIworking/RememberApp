from Library import *
import json
import os
import tkinter as tk
from tkinter import ttk
import math
import  time
from functools import partial
new_list = {}
min_width = 700

class List_maker:
    def __init__(self):
        win = main_win()
        label_1 = Main_label(win,"Come up with a new name for your new list: ", 15)
        file_name = tk.Entry(win)
        file_name.pack()
        btn1 = BTN(win, lambda:self.checking_lists_name(win,file_name.get()),"Save1")
        win.mainloop()
    def checking_lists_name(self, win, note_name):
        print(note_name)
        if len(note_name) < 1:
            print("Your name has to contain at least 1 symbol")
            message_win(win, "Your name has to contain at least 1 symbol")
        elif note_name + '.json' in os.listdir("lists"):
            message_win(win, "This name already exists",)
        else:
            win.destroy()
            writing_json(note_name, {})
            self.amountOfWords(note_name)


    def amountOfWords(self, note_name):
        win = main_win()
        label_1 = Main_label(win, "Your file has been successfully saved", 15,
                             min_width, "white", "green")
        label_2 = Main_label(win,"How many words do you wanna add?", 15)
        amount = tk.Entry(win)
        amount.pack()
        btn2 = BTN(win,lambda: self.filling_new_list(win,amount.get(), note_name), "Save2")

        win.mainloop()

    def filling_new_list(self, win, amountOfWords, note_name):
        try:
            amountOfWords = int(amountOfWords)
        except ValueError:
                message_win(win,"You didn't write a num")
        else:
            if int(amountOfWords) < 1:
                message_win(win, "You can't write a num less than 1")
                return
            elif int(amountOfWords)>29:
                message_win(win, "You wrote too big amount of words\n"
                                 "Unfortunately We couldn't make "
                                 "a scrollbar. Sorry")
                return
            win.destroy()
            win = main_win()
            label_1 = tk.Label(win, text="Fill all fields",
                               bg="#dbdbdb", font=("Arial", 15),
                               padx=20, pady=20)
            label_1.grid(row=0,column=0,columnspan=4,sticky="we")
            fields = []
            for i in range(1,amountOfWords+1):
                label_num = tk.Label(win, text=i, font=("Arial", 14),)
                label_num.grid(row=i,column=0,sticky="e")
                for j in range(1,3):
                    field = tk.Entry(win, width=34)
                    field.grid(row=i, column=j)
                    fields.append(field)
            win.grid_columnconfigure(1, minsize=200)
            win.grid_columnconfigure(2, minsize=200)
            btn3 = tk.Button(win, text='Save3',
                             command=lambda: self.list_saving(win,fields, note_name),
                             bg="#dbdbdb", font=("Arial", 14),
                             padx=20, pady=5, )
            btn3.grid(row=2, column=3, rowspan=2 ,sticky="e")
            win.mainloop()
    def list_saving(self, win,fields, note_name):
        words = []
        for i in range(len(fields)):
            if fields[i].get()=='':
                message_win(win,"You have at least 1 empty field")
                break
            elif i!=len(fields)-1 and i%2==0:
                words.append([fields[i].get(),fields[i+1].get()])
        new_dict = {}
        for i in words:
            new_dict[i[0]]=i[1]
        writing_json(note_name, new_dict)


