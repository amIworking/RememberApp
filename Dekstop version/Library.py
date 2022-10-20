
import json
import os
import tkinter as tk
from functools import partial
min_width = 700

class BTN:

    def __init__(self,win, func, text='examle',id1=1,id2=1,bg="#dbdbdb",
                font=("Arial", 14),padx=20, pady=5):
        btn = tk.Button(win, text=text,
                        command=func,
                        bg=bg, font=font,
                        padx=padx, pady=pady)
        btn.pack()
def close_win(**sev):
    print(sev)
    #win.destroy()
    for i in sev.values():
        if i == None:
            return
        i.destroy()

def btn_cl(win,args, text='examle', id1=1):
    btn = tk.Button(win, text=text,
                        command=lambda: close_win(**args),
                      bg="#dbdbdb", font=("Arial", 14),
                      padx=20, pady=5)
    btn.pack()

def main_win():
    win = tk.Tk()
    win.title("RememberApp v2.0")
    win.geometry("400x500+100+200")
    win.resizable(True, False)
    win.maxsize(1000, 600)
    win.minsize(min_width, 500)
    return win
def message_win(m_win,text,color="red", flag=False, fs = 'bold'):
    win = tk.Tk()
    win.title("RememberApp v2.0")
    win.geometry("700x100+500+400")
    win.resizable(False, False)
    message = tk.Label(win, text=text,
                    fg=color, font=("Arial", 14, fs))
    message.pack()
    if flag == False:
        btn_cl(win, {"t2":win}, "close")
    else:
        btn_cl(win, {"t1":m_win,"t2":win}, "close")
    return win

def test():
    pass