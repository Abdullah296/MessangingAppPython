from tkinter import*

master=Tk()

def e1_delete():
    e1.delete(first=0,last=100)

def master_destroy():
     master.destroy()
    

def entry_destroy():
    e1.destroy()
    

e1=Entry(master, width=35)
e1.pack()


b_erase=Button(master, text="Erase", command=e1_delete)
b_erase.pack()

b_quit_destroy=Button(master, text="Quit", command=master_destroy)
b_quit_destroy.pack()


b_delete_text=Button(master, text="Delete Entry", command=entry_destroy)
b_delete_text.pack()


master.mainloop()