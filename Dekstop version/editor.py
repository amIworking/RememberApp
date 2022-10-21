from Library import *
import os
import json
lists = os.listdir('lists')

class Editor:
    def __init__(self):
        win = main_win()
        lists = os.listdir('lists')
        label_1 = Main_label(win,"Here are all lists which exist at this moment")
        label_2 = Main_label(win, f"{lists[:]}",12)
        label_3 = Main_label(win, "Print a name of a list which you wanna edit:")

        file_name = tk.Entry(win)
        file_name.pack()
        btn1= BTN(win,lambda:self.file_check(file_name.get(),win),"Searh")
        win.mainloop()

    def file_check(self, note_name, win):
        if note_name + ".json" not in os.listdir('lists'):
            message_win(win, f"This list ({note_name}) doesn't exist. Try again")
            return
        else:

            with open(f"lists/{note_name}.json", "r") as r:
                edit_list = json.load(r)
                win.destroy()
                win = main_win()
                label_1 = Main_label(win, "Here are all word from the list")
                label_2 = Main_label(win, f"{edit_list}", 12)
                label_3 = Main_label(win, "Print a word which you wanna change:")

                word = tk.Entry(win)
                word.pack()
                btn2 = BTN(win,lambda: self.words_changing(win,note_name,edit_list,word.get()))
                btn1 = tk.Button(win, text='Search',
                                 command=lambda: self.file_check(word.get(), win),
                                 bg="#dbdbdb", font=("Arial", 14),
                                 padx=20, pady=5, )
    def words_changing(self, win,note_name,edit_list,word):
        if word not in edit_list.keys():
            message_win(win,"Your word doesn't exit")
            return
        else:
            win.destroy()
            win = main_win()
            label_1 = tk.Label(win, text=f"You choised a word '{word}'",
                               bg="#dbdbdb", font=("Arial", 15),
                               padx=20, pady=20)
            label_1.grid(row=0, columnspan=3, sticky="we")
            label_1 = tk.Label(win, text=f"Fill new fields to save changing",
                               bg="#dbdbdb", font=("Arial", 15),
                               padx=20, pady=20)
            label_1.grid(row=1,columnspan=3, sticky="we")
            label_num = tk.Label(win, text="New word:", font=("Arial", 14), )
            label_num.grid(row=2, column=0, sticky="e")
            k_word = tk.Entry(win, width=36,highlightthickness=1)
            v_word = tk.Entry(win, width=36,highlightthickness=1)
            k_word.configure(highlightbackground="black", highlightcolor="black")
            v_word.configure(highlightbackground="black", highlightcolor="black")
            k_word.grid(row=2, column=1)
            v_word.grid(row=2, column=2)
            btn3 = tk.Button(win, text='Save3',
                             command=
                             lambda: self.saving_new_word(win,note_name,edit_list,word,
                                                          k_word.get(), v_word.get()),
                             bg="#dbdbdb", font=("Arial", 14),
                             padx=20, pady=5, )
            btn3.grid(row=3, column=2, sticky="e")
            win.mainloop()

    def saving_new_word(self,win, note_name, edit_list, edit_word, new_key, new_value):
        if new_key == "" or new_value == "":
            message_win(win, "You didn't fill at least 1 field")
            return
        else:
            win = message_win(win,f"You changed {edit_word} - {edit_list[edit_word]}"
                                      f" to {new_key} - {new_value}\n"
                                   f"Your list has been successfully saved","green",True)
            edit_list.pop(edit_word)
            edit_list[new_key] = new_value
            writing_json(note_name, edit_list)


class Deleting:
    def __init__(self):
        win = main_win()
        lists = os.listdir('lists')
        label_1 = Main_label(win,"Here are all lists which exist at this moment")
        label_2 = Main_label(win, f"{lists[:]}",12)
        label_3 = Main_label(win, "Print a name of a list which you wanna delete:")
        file_name = tk.Entry(win)
        file_name.pack()
        btn1 = BTN(win, lambda: self.file_check(file_name.get(), win), "Searh")
        win.mainloop()

    def file_check(self, note_name, win):
        if note_name + ".json" not in os.listdir('lists'):
            message_win(win, f"This list ({note_name}) doesn't exist. Try again")
            return
        else:
            f_warn =  tk.Tk()
            f_warn.title("RememberApp v2.0")
            f_warn.geometry("400x200+500+400")
            f_warn.resizable(False, False)
            label_1 = tk.Label(f_warn, text=f"You're gonna delete {note_name} list"
                                         "\nAre you sure?",
                    fg="red", font=("Arial", 14))
            label_1.grid(row=0, columnspan=2, sticky="we")
            btn1 = tk.Button(f_warn, text="Yes",
                            command=lambda: self.file_delating(win,note_name,f_warn),
                            bg="#dbdbdb", font=("Arial", 14),
                            padx=20, pady=5)
            btn2 = tk.Button(f_warn, text="NO",
                            command=lambda: close_win(**{"t1": f_warn}),
                            bg="#dbdbdb", font=("Arial", 14),
                            padx=20, pady=5)
            btn1.grid(row=1,column=0)
            btn2.grid(row=1, column=1, sticky="e")

    def file_delating(self, win, note_name,f_warn):
        f_warn.destroy()
        if os.path.isfile(f"lists/{note_name}" + '.json'):
            os.remove(f"lists/{note_name}" + '.json')
            win.destroy()
            message_win(win, "Deleting was successfull", "green")
        else:
            message_win(win, f"This list ({note_name}) doesn't exist. Try again")
