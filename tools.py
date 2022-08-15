#-------------------- imports --------------------

import pickle
import hashlib
import datetime
from secrets import randbelow as rand_sec


#-------------------- classes --------------------


#-------------------- functions --------------------

def log(msg):
    #get message and add to the event log
    
    to_log = f"\n {msg} {datetime.datetime.now()}"    

    with open("blk_log.txt", "a") as lf:
        lf.write(to_log)


def hash(msg):
    #handle data to hash, verify message type and return hash value
    
    if type(msg) == str:        
        msg = str.encode(msg)
        log(f"[tools -> hash function] - string hash ")        

    elif type(msg) == int:        
        msg = msg.to_bytes(4, byteorder ="big")
        log(f"[tools -> hash function] - int hash ")        

    elif type(msg) == dict:        
        msg = pickle.dumps(msg)        
        log(f"[tools -> hash function] - dict hash ")        

    else:
        print("\n Please check your message. \n")
    
    return(hashlib.sha256(msg).hexdigest())
    
def hash_sig(M, R):

		hash = hashlib.sha256()
		hash.update(pickle.dumps(M))
		hash.update(str(R).encode())
		return int(hash.hexdigest(),16)


#-------------------- main --------------------

def test_main():
    #function created for test purposes    
    pass


if __name__ == "__main__":

    print("\n This is a module, should be imported not run \n")

    test_main()