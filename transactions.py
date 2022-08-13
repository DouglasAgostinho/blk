#-------------------- imports --------------------

import tools

#-------------------- variables --------------------


mem_pool = [{"send_add": "Sender Address", "recv_add": "Receiver Address", 
            "amount": "Amount Tx", "time_stamp": "Time Stamp",
            "tx_id": "Transaction ID", "tx_sig": "Transaction Signature"}]

blk_tx = {"send_add": "Sender Address", "recv_add": "Receiver Address", 
            "amount": "Amount Tx", "time_stamp": "Time Stamp",
            "tx_id": "Transaction ID", "tx_sig": "Transaction Signature"}


#-------------------- class --------------------
    

#-------------------- main --------------------

def test_main():
    #function used for test or Debug purposes

    print("\n Test routine started \n")

    test_msg = 123 

    print(tools.hash(test_msg))

    print("\n Test routine ended \n")

if __name__ == "__main__":   

    #print("\n just testing for now \n")
    test_main()
    