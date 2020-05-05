from tkinter import *

root = Tk()

root.wm_title("Keystroke Analysis")

mylist = []

def get_data(l):
    l.append(box1.get())
    print(l)

var1 = StringVar()
var1.set("Enter your password")
label1 = Label(root,textvariable=var1,height = 2)
label1.grid(row=0,column=0)

Username=StringVar()
box1=Entry(root,bd=4,textvariable=Username)
box1.grid(row=0,column=1)

botonA= Button(root, text = "Accept",command=lambda: get_data(mylist), width=5)
botonA.grid(row=0,column=2)

root.mainloop()