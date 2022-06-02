import random
import config
import os
from simulator.ply_dropper import drop_ply
from utils.manifest_tools import manifest_to_list
import subprocess

def parse_pc_err(out):
    raw = out.split()[-14]
    if raw == 'inf':
        psnr = 1
    else:
        psnr = raw
    return psnr

#TODO:call the pcc_error_d to compute the PSNR-D in MPEG
def external_pcc_error(input_path,output_path):
    exe = "pc_error_d"
    option1 = " --fileA=" + input_path
    option2 = " --fileB=" + output_path
    cmd = exe + option1 + option2
    print(cmd)
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print("program output:", out)
    psnr = parse_pc_err(out)
    return psnr

def compute_psnr(fi, recv_handle):
    data_root = "data"
    input_prefix = "before"
    output_prefix = "after"
    manifest_path = "manifest.json"
    chunk_list = manifest_to_list(manifest_path)
    filename = chunk_list[fi]["filename"]
    input_root = os.path.join(data_root, input_prefix)
    input_path = os.path.join(input_root, filename)
    output_root = os.path.join(data_root, output_prefix)
    output_path = os.path.join(output_root, filename)
    #TODO: The recv_handle should handle 16 blocks. Yet we will assume there is only one block at the moment
    n_points = drop_ply(input_path, output_path, recv_handle[0])
    psnr = 1
    if n_points > 0:
        psnr = external_pcc_error(input_path,output_path)
    return psnr


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

if __name__=="__main__":
    out = b'PCC quality measurement software, version 0.13.5\r\n\r\ninfile1:        data\\before\\loot_vox10_1000.ply\r\ninfile2:        data\\after\\loot_vox10_1000.ply\r\nnormal1:        \r\nsinglePass:     0\r\nhausdorff:      0\r\ncolor:          0\r\nlidar:          0\r\nresolution:     0\r\ndropDuplicates: 2\r\nneighborsProc:  1\r\naverageNormals: 1\r\nmseSpace:       1\r\nnbThreads:      1\r\n\r\nVerifying if the data is loaded correctly.. The last point is: 288 969 329\r\nReading file 1 done.\r\nVerifying if the data is loaded correctly.. The last point is: 288 969 329\r\nReading file 2 done.\r\nMinimum and maximum NN distances (intrinsic resolutions): 1, 2\r\nPeak distance for PSNR: 2\r\nPoint cloud sizes for org version, dec version, and the scaling ratio: 784142, 784142, 1\r\nNormals prepared.\r\n\r\n1. Use infile1 (A) as reference, loop over A, use normals on B. (A->B).\r\n   mse1      (p2point): 0\r\n   mse1,PSNR (p2point): inf\r\n2. Use infile2 (B) as reference, loop over B, use normals on A. (B->A).\r\n   mse2      (p2point): 0\r\n   mse2,PSNR (p2point): inf\r\n3. Final (symmetric).\r\n   mseF      (p2point): 0\r\n   mseF,PSNR (p2point): inf\r\nJob done! 13.89 seconds elapsed (excluding the time to load the point clouds).\r\n'
    print(out.split())
    mse = out.split()[-14]
    print(mse)
    parse_pc_err(out)