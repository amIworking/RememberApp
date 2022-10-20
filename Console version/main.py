from creation import *
from repeating import *
from editor import *
while True:
    print("Choose your what you want to do: ")
    print("1.Create a new list\n2.Repeat some list"
          "\n3.Edit some list\n4.Delete some list\n5.Exit")
    main_option = input()
    if main_option == "1":
        print("You chose to create a new list")
        filling_new_list()
        break
    elif main_option == "2":
        print("You chose to repeat some list")
        training()
        break
    elif main_option == "3":
        print("You chose to edit some list")
        edition()
        break
    elif main_option == "3":
        print("You chose to delete some list")
        deleting()
        break
    elif main_option == "5":
        break
    else:
        print("This option doesn't exist")
        input()