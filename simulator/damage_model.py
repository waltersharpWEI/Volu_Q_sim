import random

import config
import numpy as np

def compute_psnr(fi, recv_handle):
    return 1

def check_arrive(recv_handle):
    rh = recv_handle
    (row,col) = rh.shape
    complete_count = 0
    for i in range(row):
        complete_flag = 1
        for j in range(col):
            if rh[i][j] == 0:
                complete_flag = 0
        if complete_flag == 1:
            complete_count += 1
    return complete_count/row

def check_skip(fi, recv_handle):
    skip = 0
    if check_arrive(recv_handle) < config.skip_thresh:
        skip = 1
    else:
        skip = 0
    return skip


def network_damage(bitmap, loss_rate):
    (row,col) = bitmap.shape
    invert_loss = int(1 / loss_rate)
    for i in range(row):
        for j in range(col):
            if random.randint(0, invert_loss) == int(invert_loss/2):
                bitmap[i][j] = 0
            else:
                bitmap[i][j] = 1
    return bitmap