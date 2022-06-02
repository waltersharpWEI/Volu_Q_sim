#input, a vector of packets presence, and the ply raw file
#output, a damaged ply file

import logging
import math
import os
import numpy as np
from utils.manifest_tools import manifest_to_list

def drop_ply(raw_path, output_path, packet_presence_list):
    NUM_PACKETS = len(packet_presence_list)
    HEADER_OFFSET = 14
    output_points = 0
    with open(raw_path, 'r') as f1:
        lines = f1.readlines()
        line = lines[6]
        raw_points = int(line.split()[2])
    logging.debug("There is " + str(raw_points) + " points in input ply.")
    with open(raw_path,'r') as f1:
        lines = f1.readlines()
        N_LINES = len(lines)
        N_POINTS = N_LINES - HEADER_OFFSET
        block_len = math.floor(N_POINTS / NUM_PACKETS)
        drop_set = set([])
        j = 0
        slot_slice_temp = np.array(range(block_len))
        for packet in packet_presence_list:
            if packet == 0:
                slot = slot_slice_temp + j * block_len
                for element in slot:
                    drop_set.add(element)
            j += 1
        #logging.debug(drop_set)
        with open(output_path,'w') as f2:
            i = 0
            for line in lines:
                if i < HEADER_OFFSET:
                    #logging.debug("Header Line:" + line)
                    f2.write(line)
                else:
                    if i in drop_set:
                        #This line is just for stub
                        _stub = 0
                        #logging.debug("Dropping Line " + str(i) + " : " + line)
                    else:
                        f2.write(line)
                        output_points += 1
                i += 1
    return output_points





if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    packet_present = [0,0,0,0,0,0,0,1]
    data_root = "../data"
    input_prefix = "before"
    output_prefix = "after"
    manifest_path = "../manifest.json"
    chunk_list = manifest_to_list(manifest_path)
    for chunk in chunk_list:
        filename = chunk['filename']
        print(filename)
        input_root = os.path.join(data_root, input_prefix)
        input_path = os.path.join(input_root, filename)
        output_root = os.path.join(data_root, output_prefix)
        output_path = os.path.join(output_root, filename)
        n_points = drop_ply(input_path, output_path, packet_present)
        if n_points > 0:
            logging.debug("The output file has " + str(n_points) + " points")
