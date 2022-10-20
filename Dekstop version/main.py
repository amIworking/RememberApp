from Library import *
from creation import *
from repeating import *
from editor import *
import tkinter as tk
win = tk.Tk()
win.title("RememberApp v2.0")
win.geometry("400x500")
win.resizable(True,False)
win.maxsize(1000,700)
min_width = 500
win.minsize(min_width,500)
main_label = tk.Label(win, text="Choose what you want to do: ",
                      bg="#dbdbdb", font=("Arial", 16),
                      padx=20, pady=20, width=min_width)
main_label.pack()

btn1 = BTN(win,List_maker,"1.Create a new list")
btn2 = BTN(win,Training,"2.Repeat some list")
btn3 = BTN(win,test,"3.Edit some list")
btn4 = BTN(win,test,"4.Delete some list")
btn5 = BTN(win,lambda:win.destroy(),"5.Exit")



win.mainloop()
