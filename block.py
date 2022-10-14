#------------------------------ imports ------------------------------

import time
import json
import hashlib

#------------------------------ variables ------------------------------

blk_hd = {"version": "0000", "prev_hx": "0xabc", "nonce": "0xabc"}
blk_ft = {"m_add": "0xabc", "hd_hx": "0xabc", "tx_hx": "0xabc"}

blk = []
tx_list = []

hx_list = []

hx_cmp = "000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"



def mnr(mem_pool):
      
    hx_nonce = 0

    st_time = time.time()
    
    blk.append(blk_hd)
    blk.append(blk_ft)
    blk.append(mem_pool)
    
    hx_dict = json.dumps(blk, indent=2).encode("utf-8")
        
    print("\n\n")
    print(hx_dict)
    print("\n\n")
        
    hx = hashlib.sha256(hx_dict)
    #hx = blk     
                       
    while True:        
        
        hx_res = hx.hexdigest()
        if hx_res < hx_cmp:
            
            print("smaller")
            #print(hx_res)
            #print(hx_nonce)
            hx_list.append(hx_res)
            hx_list.append(hx_nonce)
            print(hx_list)
            print(time.time() - st_time)
            result = (True, hx_nonce)
            break
            
        else:
            print("higher")
            print(hx_res)
            hx.update(hx_nonce.to_bytes(4, byteorder="big"))
            hx_nonce += 1
                
    return(result)