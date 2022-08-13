#-------------------- imports --------------------

import hashlib


#-------------------- classes --------------------


#-------------------- functions --------------------

def hash(msg):
    #handle data to hash, verify message type and return hash value
    
    if type(msg) == str:
        print("string")
        msg = str.encode(msg)
    elif type(msg) == int:
        print("int")
        msg = msg.to_bytes(4, byteorder ="big")
    else:
        print("\n Please check your message. \n")

    return(hashlib.sha256(msg).hexdigest())


#-------------------- main --------------------

def test_main():
    #function created for test purposes
    pass


if __name__ == "__main__":

    print("\n This is a module, should be imported not run \n")

    test_main()