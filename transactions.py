#-------------------- imports --------------------
from hashlib import new
import datetime
import tools

#-------------------- variables --------------------

#block tx model
#
# blk_tx = {"send_add": "Sender Address", "recv_add": "Receiver Address", 
#             "amount": "Amount Tx", "time_stamp": "Time Stamp",
#             "tx_id": "Transaction ID", "tx_sig": "Transaction Signature"}


#-------------------- class --------------------

class Transaction:
        
    def __init__(self, send_add, recv_add, amount):
        self.send_add = send_add
        self.recv_add = recv_add
        self.amount = amount
        self.time = str(datetime.datetime.now())

    def new_tx(self):
        initial_tx = {"send_add": self.send_add, "recv_add": self.recv_add, 
            "amount": self.amount, "time_stamp": self.time}
        
        tx_id = tools.hash(initial_tx)

        new_tx = {"send_add": self.send_add, "recv_add": self.recv_add, 
            "amount": self.amount, "time_stamp": self.time, "tx_id": tx_id}
        
        tools.log("[Transactions -> new_tx] - New transaction created")
        return(new_tx)

#-------------------- main --------------------

def test_main():
    #function used for test or Debug purposes

    print("\n Test routine started \n")

    

    for i in range(3):
        tx = Transaction(i*10, i*20, i)
        print(tx.new_tx())

    

    print("\n Test routine ended \n")

if __name__ == "__main__":   

    #print("\n just testing for now \n")
    test_main()
    