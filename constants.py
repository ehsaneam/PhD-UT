# RCCO, (C) Mahdi Dolati. License: AGPLv3
class Const:
    VNF_NUM = 50
    VNF_CPU = [0.25, 0.5]
    VNF_RAM = [0.25, 0.5]
    VNF_LAYER = [5, 12]  # [5, 12]
    TAU1 = [5, 8]
    TAU2 = [8, 21]
    LAYER_NUM = 200
    LAYER_SIZE = [50, 350]  # [2, 70]
    MS_DELAY = [500, 2000]
    ALPHA_RANGE = [0.8, 1.05]
    LAMBDA_RANGE = [1, 5]
    # LINK_BW = [10000, 20000]

    # Entity Numbers
    BTS_NUM  = 10
    EDGE_NUM = 7
    REG_NUM  = 1

    # Edge Server Values
    EDGE_CPU = 240   # GHz
    EDGE_RAM = 256   # GB
    EDGE_DSK = 10000 # GB

    # Regional Server Values
    REG_CPU = 4000   # GHz
    REG_RAM = 4000   # GB
    REG_DSK = 160000 # GB