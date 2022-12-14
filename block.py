#------------------------------ imports ------------------------------
import os
import platform
import time
import json
import tools
import pickle
import hashlib
import datetime
from tkinter import Pack

#------------------------------ constants ------------------------------

# get the current running os to determine with PATH to follow
OS_NAME = platform.system()

if OS_NAME.lower() == "linux":
    PATH = r"/home/ice/Documents/python/blk/data/"
else:
    PATH = r"C:\Users\iceli\OneDrive\Documentos\python\blk\data\\"

#------------------------------ variables ------------------------------

blk_hd = {"version": "0000", "prev_hx": "0xabc", "nonce": 0}
blk_ft = {"m_add": "0xabc", "hd_hx": "0xabc", "tx_hx": "0xabc"}
last_block_hx = "0xabc"
tx_list = []


# Chain difficulty
hx_cmp = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

#------------------------------ Functions and Classes definition ------------------------------

def block_read(block):

    with open(f"{PATH}{block}", "rb") as fb:
            print(pickle.loads(fb.read()))
            

def block_find(path):
    # Search in the PATH for blocks stored
        
    blk_list = []

    for root, dirs, files in os.walk(path):
        for file in files:
            blk_list.append(file)
            #print(file)
            #print(sorted(files))
        
        blk_list = sorted(blk_list, key=lambda x: int(x.split('_')[0]))
        
    return(blk_list)
    

def block_hx_ctrl():
    # Update the file with all block hashes

    global last_block_hx
    blocks = block_find(PATH)
    hx_blocks = []

    for block in blocks:
         with open(f"{PATH}{block}", "rb") as fb:
            blk = pickle.loads(fb.read())
            hx_dict = json.dumps(blk, indent=2).encode("utf-8")    
            hx_res = hashlib.sha256(hx_dict).hexdigest()
            hx_blocks.append(hx_res)
            print(block, hx_res)

    with open("block_hx_control.txt", "r") as bf:
        lines = bf.read().split()
        for line in lines:
            if line in hx_blocks:
                last_block_hx = line
            else:
                print(f"missing hash {line}")           
            
                   
def block_pack(blk):  
    # Get Header, transactions and foot to create the block

    b_list = block_find(PATH) 
    blk_name = "0_blk.txt"
    i = 0
    
    for i in range(len(b_list)):
        if (f"{i}_blk.txt") in b_list:
            i += 1

    blk_name = f"{i}_blk.txt"
    
    with open(f"{PATH}{blk_name}", "wb") as lf:    
        lf.write(pickle.dumps(blk))
    
    return(blk_name)
    

def block_validate(blk_name):
    # Validate the data in the received block
    # Hash and compare nonce

    with open(f"{PATH}{blk_name}", "rb") as f:
        blk = pickle.loads(f.read())

    hx_dict = json.dumps(blk, indent=2).encode("utf-8")    
    hx_res = hashlib.sha256(hx_dict).hexdigest()

    if hx_res < hx_cmp:
        print("Valid BLock")
        return(blk[1])

    else:
        print("Invalid block")


def blk_bytes(mem_pool):
    # Pack block data and convert to bytes

    global last_block_hx
    blk_hd["prev_hx"] = last_block_hx
    blk = [blk_hd, mem_pool, blk_ft, hx_cmp]

    hx_dict = json.dumps(blk, indent=2).encode("utf-8")
        
    return(hashlib.sha256(hx_dict).hexdigest(), blk)

"""
def mnr(mem_pool):
    # Block "mined" by increase the nonce until it reaches the difficulty

    #st_time = time.time()
    global last_block_hx 

    while True:            
        hx_res, blk = blk_bytes(mem_pool)
        
        if hx_res < hx_cmp:    
            hx_list.append(hx_res)
            hx_list.append(blk_hd["nonce"])
            result = (True, blk_hd["nonce"])
            last_block_hx = hx_res

            with open("block_hx_control.txt", "a") as bhc:    
                bhc.write(f"{last_block_hx} \n")

            blk_name = block_pack(blk)
            break
            
        else:
            blk_hd["nonce"] += 1
                
    return(result, blk_name)

"""

if __name__ == "__main__":
    block_find(PATH)
    block_read(input("insert block name: "))