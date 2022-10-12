from tkinter import *
from tkinter import ttk

class Scr1:

    def __init__(self, master):
        
        self.send_label = Label(master, text = "Sender Address")
        self.recv_label = Label(master, text = "Receiver Address")
        self.amnt_label = Label(master, text = "Amount")

        self.send_entry = Entry(master, width = "20")
        self.recv_entry = Entry(master, width = "20")
        self.amnt_entry = Entry(master, width = "20")

        self.send_button = Button(master, text = "Send", command = self.tx)
        self.clear_button = Button(master, text = "Clear", command = self.clr_fields)

    def plot(self):
        self.send_label.grid(row=0, column=0)
        self.send_entry.grid(row=0, column=1)

        self.recv_label.grid(row=1, column=0)
        self.recv_entry.grid(row=1, column=1)

        self.amnt_label.grid(row=3, column=0)
        self.amnt_entry.grid(row=3, column=1)

        self.clear_button.grid(row=4, column=0)
        self.send_button.grid(row=4, column=1)    

    def clr_fields(self):
        self.send_entry.delete(0, END)
        self.recv_entry.delete(0, END)
        self.amnt_entry.delete(0, END)

    def tx(self):
        print(f"You are sending {self.amnt_entry.get()} to {self.recv_entry.get()}")




root = Tk()

root.title("Le chain")
root.geometry("400x300")

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text = "Transactions")
tabControl.add(tab2, text = "Mem Pool")
tabControl.pack(expand = 1, fill = "both")

new_scr = Scr1(tab1)

new_scr.plot()

root.mainloop()