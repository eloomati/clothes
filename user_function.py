from tkinter import *

class Menu:
    # initializing object
    root = Tk()
    # make size of window
    root.geometry('200x200')

    def show():
        label.config(text = clicked.get() )
    # Options of menu
    options = [
        'A',
        'B',
        'C'
    ]
    # type of data of menu
    clicked = StringVar()
    # option on begin of program
    clicked.set('A')
    # init menu
    drop = OptionMenu( root, clicked, *options)
    drop.pack()
    # init button
    button = Button( root, text='Click Me', command = show).pack()
    # create label
    label = Label(root, text = ' ')
    label.pack()
    #execute
    root.mainloop()


master = Tk()
e = Entry(master)
e.pack()

e.focus_set()

def callback():
    print(e.get()) # This is the text you may want to use later

b = Button(master, text = "OK", width = 10, command = callback)
b.pack()

mainloop()

from tkinter import *











root = Tk()
# make size of window
root.geometry('200x200')
e = Entry(root)
e.pack()

def show():
    label.config(text=clicked.get())

def callback():
    print(e.get()) # This is the text you may want to use later



b = Button(root, text = "OK", width = 10, command = callback)
# Options of menu
options = [
    'A',
    'B',
    'C',
    b.pack()
]

# type of data of menu
clicked = StringVar()
# option on begin of program
clicked.set('A')
# init menu
drop = OptionMenu(root, clicked, *options)
drop.pack()
# init button
button = Button(root, text='Click Me', command=show).pack()
# create label
label = Label(root, text=' ')

label.pack()

# execute
root.mainloop()