import time
import block
from tkinter import *
from tkinter import ttk
import transactions as tx
from concurrent.futures import ThreadPoolExecutor 

#-------------------- Global --------------------

mem_pool = [{"send_add": "Sender Address", "recv_add": "Receiver Address", 
             "amount": "Amount Tx", "time_stamp": "Time Stamp",
             "tx_id": "Transaction ID", "tx_sig": "Transaction Signature"},]



new_tx = tx.Transaction()

def update_pool(updt_pool):
    #print("updating pool")
    #print(updt_pool)
    print(f" Memory pool before {mem_pool}")
    for item in updt_pool:
        
        #print(f" item is {item}")
        for i in mem_pool:
            #print(f"item is {item} and mem_pool[i] is {i}")
            
            print(mem_pool)
            if i == item:
                mem_pool.remove(item)
            
    print(f" Memory pool after {mem_pool}")

    tx_to_block()

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
        #print(f"You are sending {self.amnt_entry.get()} to {self.recv_entry.get()}")
        signed_tx = new_tx.new_tx(self.send_entry.get(), self.recv_entry.get(), self.amnt_entry.get()) 
        mem_pool.append(signed_tx)
        #print(signed_tx)


def tx_to_block():
    
    mem_text = Text(tab2, height = 35, width = 95)
    mem_label = Label(tab2, text = "Mem Pool")

    #mem_label.grid(row = 10, column = 10)
    mem_text.grid(row = 11, column = 0)
    print("test")
    result = (False, 0)
    print(result)
    while True:
        mem_text.delete(1.0, END) 
        for item in mem_pool:       
            mem_text.insert(END, item)
            mem_text.insert(END, "\n\n")
        time.sleep(1)
        if len(mem_pool) > 0 and result[1] == 0:
            print("bigger")
            result, blk_name = block.mnr(mem_pool)
            break            
        else:
            print("Not ready")
            result = (False, 0)
    update_pool(block.block_validate(blk_name))
    

root = Tk()

root.title("Le chain")
root.geometry("800x600")

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text = "Transactions")
tabControl.add(tab2, text = "Mem Pool")
tabControl.pack(expand = 1, fill = "both")

new_scr = Scr1(tab1)

new_scr.plot()

win = Toplevel(root)

with ThreadPoolExecutor(max_workers = 3) as tpe:

    fut_loop_01 = tpe.submit(tx_to_block)

    root.mainloop()