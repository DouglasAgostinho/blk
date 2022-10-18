#------------------------------ imports ------------------------------
import block
import platform

#------------------------------ constants ------------------------------

# get the current running os to determine with PATH to follow
OS_NAME = platform.system()

if OS_NAME.lower() == "linux":
    PATH = r"/home/ice/Documents/python/blk/data/"
else:
    PATH = r"C:\Users\iceli\OneDrive\Documentos\python\blk\data\\"

#------------------------------ Functions and Classes definition ------------------------------

def intialization ():
    # Initialization function        
    blocks = block.block_find(PATH)

    print(blocks)

    block.block_hx_ctrl()
