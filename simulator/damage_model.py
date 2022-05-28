import config

def compute_psnr(fi, recv_handle):
    return 1

def check_arrive(recv_handle):
    return 1

def check_skip(fi, recv_handle):
    skip = 0
    if check_arrive(recv_handle) < config.skip_thresh:
        skip = 1
    else:
        skip = 0
    return skip