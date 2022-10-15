#------------------------------ imports ------------------------------
import os
import time
import json
import pickle
import hashlib
import datetime

#------------------------------ constants ------------------------------
PATH = r"C:\Users\iceli\OneDrive\Documentos\python\blk\data\\"
#------------------------------ variables ------------------------------

blk_hd = {"version": "0000", "prev_hx": "0xabc", "nonce": 0}
blk_ft = {"m_add": "0xabc", "hd_hx": "0xabc", "tx_hx": "0xabc"}

blk_list = []
tx_list = []

hx_list = []

hx_cmp = "000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

def block_find(name, path):
    for root, dirs, files in os.walk(path):
        blk_list.append(os.path.join(name))
        


def block_pack(blk):   
    
    with open(f"{PATH}blk_0.txt", "wb") as lf:
        print("file opened")
        print(f"{PATH}blk_0.txt")     
        print(blk)

        lf.write(pickle.dumps(blk))
    

def block_validadte():

    with open(f"{PATH}blk_0.txt", "rb") as f:
        blk = pickle.loads(f.read())

    hx_dict = json.dumps(blk, indent=2).encode("utf-8")    

    hx_res = hashlib.sha256(hx_dict).hexdigest()

    if hx_res < hx_cmp:
        print("Valid BLock")
    else:
        print("Invalid block")

def blk_bytes(mem_pool):
    
    blk = [blk_hd, mem_pool, blk_ft, hx_cmp]
    print(blk)
    
    hx_dict = json.dumps(blk, indent=2).encode("utf-8")
        
    return(hashlib.sha256(hx_dict).hexdigest(), blk)


def mnr(mem_pool):

    st_time = time.time()
                       
    while True:        
        
        hx_res, blk = blk_bytes(mem_pool)
        #print(f"blk is {blk}")
        #print(hx_res)
        if hx_res < hx_cmp:
            
            print("smaller")
            hx_list.append(hx_res)
            hx_list.append(blk_hd["nonce"])
            print(hx_list)
            print(time.time() - st_time)
            result = (True, blk_hd["nonce"])
            block_pack(blk)
            break
            
        else:
            print("higher")
            blk_hd["nonce"] += 1
            print(blk_hd["nonce"])
                
    return(result)



if __name__ == "__main__":
    pass