import threading
import time
import pandas as pd
import numpy as np
import logging
import config



def pull_frame(fi):
    Interval = 1 / config.FR
    time.sleep(Interval)
    #TODO:damage the file according to the trace loss
    return

def udp_sim():
    T = config.T
    fi = 0
    psnrs = []
    skips = []
    frame_nos = range(T)
    while fi < T:
        recv_handle = pull_frame(fi)
        psnr = compute_psnr(fi, recv_handle)
        skips = check_skip(fi, recv_handle)
        psnrs.append(psnr)
        skips.append(skips)
        fi += 1
    print("All Done.")
    stalls = np.zeros(T)
    df = pd.DataFrame({"frame_no":frame_nos,
                       "stall":stalls,
                       "psnr":psnrs,
                       "skip":skips})
    df.to_csv("udp_stall.csv",index=False)
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    t1 = threading.Thread(target=udp_sim())
