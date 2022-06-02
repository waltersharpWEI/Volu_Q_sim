import threading
import time
import pandas as pd
import numpy as np
import logging

import config
from simulator.damage_model import offline_psnr, check_skip, network_damage, damage_file


def pull_frame(fi):
    Interval = 1 / config.FR
    time.sleep(Interval)
    recv_bitmap = np.ones((16,10))
    # TODO:replace 0.1 with actual loss in network trace
    recv_bitmap = network_damage(recv_bitmap, 0.1)
    #logging.debug(recv_bitmap)
    return recv_bitmap


def udp_sim():
    T = config.T
    fi = 0
    psnrs = []
    skips = []
    frame_nos = range(T)
    while fi < T:
        logging.debug("Start pulling frame " + str(fi) + ".")
        recv_handle = pull_frame(fi)
        n_points = damage_file(fi, recv_handle)
        skip = check_skip(fi, recv_handle)
        #The psnr will be updated in the offline_psnr
        #In the two-pass fashion
        psnrs.append(1)
        skips.append(skip)
        fi += 1

    print("All Done.")
    stalls = np.zeros(T)
    df = pd.DataFrame({"frame_no":frame_nos,
                       "stall":stalls,
                       "psnr":psnrs,
                       "skip":skips})
    print("Computing PSNR")
    df = offline_psnr(df)
    print("PSNR is computed")
    df.to_csv("udp_qos.csv",index=False)
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    t1 = threading.Thread(target=udp_sim())
