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
import time

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
        # image_hash = imagehash.average_hash(image)
        image_hash = imagehash.phash(image)
        image_hashes[image_hash].append(image_path)

        if len(image_hashes[image_hash]) > 1:
            duplicate_dict[image_hash] = list(set(duplicate_dict[image_hash] + image_hashes[image_hash]))
            print("\nfind duplicate : (hash)")
            for item in duplicate_dict[image_hash]:
                print(item)

    duplicate_list = [image_list for image_list in duplicate_dict.values()]

    return duplicate_list


def dim_filter(image_paths):
    '''寻找相同图片(尺寸)'''
    image_dims = defaultdict(list)
    duplicate_dict = defaultdict(list)
    for image_path in image_paths:
        image = Image.open(image_path)
        width, height = image.size
        image_dim = str(width) + "-" + str(height)
        image_dims[image_dim].append(image_path)

        if len(image_dims[image_dim]) > 1:
            duplicate_dict[image_dim] = list(set(duplicate_dict[image_dim] + image_dims[image_dim]))
            print("\nfind duplicate (dimension): ")
            for item in duplicate_dict[image_dim]:
                print(item)

    duplicate_list = [image_list for image_list in duplicate_dict.values()]

    return duplicate_list


def size_filter(image_paths):
    '''寻找相同图片(大小)'''
    '''实际测试发现了一些分辨率和尺寸都相同但大小不同的图片，因此不采用这个方法'''
    image_size_list = defaultdict(list)
    duplicate_dict = defaultdict(list)
    for image_path in image_paths:
        image = Image.open(image_path)
        width, height = image.size
        img_size = os.path.getsize(image_path)
        image_size_list[img_size].append(image_path)

        if len(image_size_list[img_size]) > 1:
            duplicate_dict[img_size] = list(set(duplicate_dict[img_size] + image_size_list[img_size]))
            print("\nfind duplicate (size): ")
            for item in duplicate_dict[img_size]:
                print(item)

    duplicate_list = [image_list for image_list in duplicate_dict.values()]

    return duplicate_list


# 表情包查重
sticker_list = [img for img in get_file(sticker_path)]
duplicate_list_dim = dim_filter(sticker_list)
duplicate_list_hash = []
for list_dim in duplicate_list_dim:
    if not hash_filter(list_dim) == []:
        duplicate_list_hash.append(hash_filter(list_dim)[0])
duplicate_sticker_list = duplicate_list_hash


# 图片查重
image_list = [img for img in get_file(image_path)]
duplicate_list_dim = dim_filter(image_list)
duplicate_list_hash = []
for list_dim in duplicate_list_dim:
    if not hash_filter(list_dim) == []:
        duplicate_list_hash.append(hash_filter(list_dim)[0])
duplicate_image_list = duplicate_list_hash


# 写入结果
duplicate_list = {
    "sticker": duplicate_sticker_list,
    "image": duplicate_image_list
}
with open(result_json, 'w', encoding="utf-8") as file:
    js_str = json.dumps(duplicate_list, ensure_ascii=False)
    file.write(js_str)


del_list = duplicate_sticker_list + duplicate_image_list

wait_here = input("\n\nFind Find %d sets of duplicate images.\n\
Press Enter to delete duplicate images. Press Ctrl+C to exit.\n\
It is recommended to check './output/duplicate.json' before deleting ..." %len(del_list))



for dp_list in del_list:
    for image in dp_list[1:]:
        print("delete: %s" % image)
        os.remove(image)
