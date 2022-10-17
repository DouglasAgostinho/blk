import block

#------------------------------ constants ------------------------------
PATH = r"C:\Users\iceli\OneDrive\Documentos\python\blk\data\\"

def intialization ():
        
    blocks = block.block_find(PATH)

    print(blocks)

    block.block_hx_ctrl()
