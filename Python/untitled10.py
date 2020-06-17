from tkinter import * 
 
root = Tk()
 
def returnEntry(arg=None):
    result = myEntry.get()
    resultLabel.config(text=result)
    myEntry.delete(0,END)
 
# Create the Entry widget
myEntry = Entry(root, width=20)
#myEntry.focus()
#myEntry.bind("<Return>",returnEntry)
myEntry.pack()
 
# Create the Enter button
enterEntry = Button(root, text= "Enter", command=returnEntry)
enterEntry.pack()
 
# Create and emplty Label to put the result in
resultLabel = Label(root, text = "")
resultLabel.pack()
 
 
root.geometry("+750+400")
 
root.mainloop()