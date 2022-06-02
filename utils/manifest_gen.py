import os
import json

path = "../data/before"
dirs = os.listdir(path)

data = []

# 输出所有文件和文件夹
for file in dirs:
    print (file)
    element = {"filename":file}
    data.append((element))

print(data)

with open('manifest.json', 'w') as f:
    json.dump(data, f)