#------------------------------ imports ------------------------------
import time
import init
import block
from tkinter import *
from tkinter import ttk
import transactions as tx
from concurrent.futures import ThreadPoolExecutor 

#-------------------- Global --------------------

# Memory pool will be a list of dictionaries with all valid transactions

mem_pool = [{"send_add": "Sender Address", "recv_add": "Receiver Address", 
             "amount": "Amount Tx", "time_stamp": "Time Stamp",
             "tx_id": "Transaction ID", "tx_sig": "Transaction Signature"},]


hx_list = []

#-------------------- Functions and Classes Definition --------------------

# Create a new object Transaction - to create / sign & validate transactions (tx)
new_tx = tx.Transaction()


def update_pool(updt_pool):
    # Receive a valid block and remove from the mem pool the transactions published in it 
    global mem_pool

    for item in updt_pool:
        for i in mem_pool:            
            if i == item:
                mem_pool.remove(item)

    # After Memory pool udate, it make the program works in the next block    
    tx_to_block()


class Scr:
    # class for the Screen objects (Main windows initially)
    global mem_pool

    def __init__(self):
        # Class initialization(main variables definiton)

        # Initial declaration for program windows

        self.root = Tk()
        self.root.title("Le chain")
        self.root.geometry("800x600")

        #Initial declaration for windows Tabs

        self.tabControl = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text = "Transactions")
        self.tabControl.add(self.tab2, text = "Mem Pool")
        

        self.mem_text = Text(self.tab2, height = 35, width = 95)
        self.mem_label = Label(self.tab2, text = "Mem Pool")
        

        self.send_label = Label(self.tab1, text = "Sender Address")
        self.recv_label = Label(self.tab1, text = "Receiver Address")
        self.amnt_label = Label(self.tab1, text = "Amount")

        self.send_entry = Entry(self.tab1, width = "20")
        self.recv_entry = Entry(self.tab1, width = "20")
        self.amnt_entry = Entry(self.tab1, width = "20")

        self.send_button = Button(self.tab1, text = "Send", command = self.tx)
        self.clear_button = Button(self.tab1, text = "Clear", command = self.clr_fields)


    def plot(self):
        # Configure how the window will be displayed

        self.tabControl.pack(expand = 1, fill = "both")
        
        self.mem_text.grid(row = 11, column = 0)   

        self.send_label.grid(row=0, column=0)
        self.send_entry.grid(row=0, column=1)

        self.recv_label.grid(row=1, column=0)
        self.recv_entry.grid(row=1, column=1)

        self.amnt_label.grid(row=3, column=0)
        self.amnt_entry.grid(row=3, column=1)

        self.clear_button.grid(row=4, column=0)
        self.send_button.grid(row=4, column=1)    
        
        # Windows on top of main screen for program updates.
        self.win = Toplevel(self.root)

        self.update_mem_pool()

        self.root.mainloop()

    def update_mem_pool(self):
        # Loop to monitor MemPool size
        
        self.mem_text.delete(1.0, END) 

        # Display the items in memory pool in the second tab
        for item in mem_pool:       
            self.mem_text.insert(END, item)
            self.mem_text.insert(END, "\n\n")
        
        self.root.after(1000, self.update_mem_pool)
        

    def clr_fields(self):
        # Clean the entry fields

        self.send_entry.delete(0, END)
        self.recv_entry.delete(0, END)
        self.amnt_entry.delete(0, END)

    def tx(self):
        # Initiate a new transaction (tx)
        
        signed_tx = new_tx.new_tx(self.send_entry.get(), self.recv_entry.get(), self.amnt_entry.get()) 
        mem_pool.append(signed_tx)
        print("add")
        


def mnr():
    # Block "mined" by increase the nonce until it reaches the difficulty

    global mem_pool
    #st_time = time.time()
        
    while True:            
        hx_res, blk = block.blk_bytes(mem_pool)
        
        if hx_res < block.hx_cmp:    
            hx_list.append(hx_res)
            hx_list.append(block.blk_hd["nonce"])
            result = (True, block.blk_hd["nonce"])
            block.last_block_hx = hx_res

            with open("block_hx_control.txt", "a") as bhc:    
                bhc.write(f"{block.last_block_hx} \n")

            blk_name = block.block_pack(blk)
            break
            
        else:
            block.blk_hd["nonce"] += 1
            to_print = block.blk_hd["nonce"]
            print(f"nonce is: {to_print}")
                
    return(result, blk_name)


def tx_to_block():
    # Main function that defines if the MemPool is ready
    # If ready it initiate the block creation

    result = (False, 0)
    
    while True:
        # Loop to monitor MemPool size

        # If one valid transaction is in memory pool initiate block creation
        if len(mem_pool) > 4 and result[1] == 0:
            #print("bigger")
            result, blk_name = mnr()
            break   

        # If not, continue
        else:
            #print("Not ready")
            result = (False, 0)

    # Use the return of block validation function as input for 
    # mem pool update
    update_pool(block.block_validate(blk_name))


def aux_functions():
    # Initializing screen
    
    new_scr = Scr()
    new_scr.plot()
    #new_scr.update_mem_pool()
    

#-------------------- Program begin --------------------

# System routines and auxiliaries initialization
init.intialization()


# Thread handler initialization
with ThreadPoolExecutor(max_workers = 3) as tpe:

    # initialize the memory pool monitoring as a new Thread
    fut_loop_01 = tpe.submit(tx_to_block)
    fut_loop_02 = tpe.submit(aux_functions)

    
