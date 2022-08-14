#-------------------- imports --------------------

import tools
import datetime
import schnorr

#-------------------- variables --------------------

#       block tx model
#
# blk_tx = {"send_add": "Sender Address", "recv_add": "Receiver Address", 
#             "amount": "Amount Tx", "time_stamp": "Time Stamp",
#             "tx_id": "Transaction ID", "tx_sig": "Transaction Signature"}


#-------------------- class --------------------

class Transaction:    
        
    def __init__(self):        
        self.time = str(datetime.datetime.now())
        self.signature = schnorr.Signature(1)

    def new_tx(self, send_add, recv_add, amount):
        self.send_add = send_add
        self.recv_add = recv_add
        self.amount = amount

        initial_tx = {"send_add": self.send_add, "recv_add": self.recv_add, 
            "amount": self.amount, "time_stamp": self.time}
        
        tx_id = tools.hash(initial_tx)

        new_tx = {"send_add": self.send_add, "recv_add": self.recv_add, 
            "amount": self.amount, "time_stamp": self.time, "tx_id": tx_id}

        tx_signature = self.signature.sign(new_tx)

        signed_tx = {"send_add": self.send_add, "recv_add": self.recv_add, 
            "amount": self.amount, "time_stamp": self.time, "tx_id": tx_id,
            "tx_sig": tx_signature}
        
        tools.log("[Transactions -> new_tx] - New transaction created")
        return(signed_tx)

    def check_tx(self, tx):

        msg = {"send_add": tx["send_add"], "recv_add": tx["recv_add"], 
             "amount": tx["amount"], "time_stamp": tx["time_stamp"], "tx_id": tx["tx_id"]}

        msg_sig = tx["tx_sig"]       

        self.signature.verify(msg, msg_sig[0], msg_sig[1])

            
#-------------------- main --------------------

def test_main():
    #function used for test or Debug purposes

    print("\n Test routine started \n")

    

    for i in range(1):
        tx = Transaction()

        tx_created = tx.new_tx(i*10, i*20, i)
        #print(tx_created)
        tx.check_tx(tx_created)

        

        

    

    print("\n Test routine ended \n")

if __name__ == "__main__":   

    #print("\n just testing for now \n")
    test_main()
    