#created on 28 May 2022.
#The Volumetric Video Simulator
#Which simulate the tcp pull process
#and output the stalling time of each frame
#Input: The network trace; file_manefest;
#Output: The stalling time list
import threading
import time
import pandas as pd
import numpy as np
import logging

import config

def pull_frame(fi):
    size = 400
    th = 10000
    time.sleep(size/th)
    return

def tcp_sim():
    T = config.T
    FR= config.FR
    Interval = 1/FR
    fi = 0
    t0 = time.time()
    stalls = []
    frame_nos = range(T)
    while fi < T:
        pull_frame(fi)
        ts = time.time()-t0
        if ts > Interval:
            stall = ts - Interval
        else:
            stall = 0
        logging.debug("STALL: " + str(fi) + ":" + str(stall))
        stalls.append(stall)
        fi += 1
        t0 = time.time()
    print("All Done.")
    psnrs = np.ones(T)
    skips = np.zeros(T)
    df = pd.DataFrame({"frame_no":frame_nos,
                       "stall":stalls,
                       "psnr":psnrs,
                       "skip":skips})
    df.to_csv("tcp_qos.csv",index=False)
    return


if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    t1 = threading.Thread(target=tcp_sim())
