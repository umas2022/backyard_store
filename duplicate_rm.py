'''
图片去重
对比图片哈希, 只能找出像素完全相同的图片
'''

import json
import os
from PIL import Image
import imagehash  # pip install imagehash
from collections import defaultdict
import cv2
import numpy as np
import skimage.metrics
import skimage.measure

import sys
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)


# auto_rm = False
result_json = os.path.normpath(os.path.join(script_path, "output/duplicate.json"))
sticker_path = os.path.normpath(os.path.join(script_path, "storage/sticker"))
image_path = os.path.normpath(os.path.join(script_path, "storage/image"))

def get_file(path_in):
    '''所有层级文件遍历'''
    for root, dirs, files in os.walk(path_in):
        for fileName in files:
            if fileName == ".gitkeep":
                continue
            full_path = os.path.normpath(os.path.join(root, fileName))
            yield full_path


def hash_filter(image_paths):
    '''寻找相同图片(哈希)'''
    image_hashes = defaultdict(list)
    duplicate_dict = defaultdict(list)
    for image_path in image_paths:
        image = Image.open(image_path)
        image_hash = imagehash.average_hash(image)
        image_hashes[image_hash].append(image_path)

        if len(image_hashes[image_hash]) > 1:
            duplicate_dict[image_hash] = list(set(duplicate_dict[image_hash] + image_hashes[image_hash]))
            print("\nfind duplicate : ")
            for item in duplicate_dict[image_hash]:
                print(item)

    duplicate_list = [image_list for image_list in duplicate_dict.values()]

    return duplicate_list



# 表情包查重
sticker_list = [img for img in get_file(sticker_path)]
duplicate_sticker_list = hash_filter(sticker_list)


# 图片查重
image_list = [img for img in get_file(image_path)]
duplicate_image_list = hash_filter(image_list)


# 写入结果
duplicate_list = {
        "sticker": duplicate_sticker_list,
        "image": duplicate_image_list
    }
with open(result_json, 'w', encoding="utf-8") as file:
    js_str = json.dumps(duplicate_list, ensure_ascii=False)
    file.write(js_str)

