'''
编辑tag
'''

import os
import json
import time

import sys
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)


# 编辑json文件路径
json_dir = os.path.normpath(os.path.join(script_path, "edit_tag"))

# 后端域名
store_url = "https://raw.githubusercontent.com/umas2022/backyard_store/main/"


def get_file(path_in):
    '''文件遍历'''
    for root, dirs, files in os.walk(path_in):
        for fileName in files:
            yield fileName


for edit_file in get_file(json_dir):
    if edit_file==".gitkeep":
        continue
    with open(os.path.join(json_dir, edit_file), "r", encoding="utf-8")as edit_jsons:
        edit_jsons = json.load(edit_jsons)
        merged_list = {}
        for i in range(len(edit_jsons)):

            # 首先合并列表
            path_old = os.path.normpath(edit_jsons[i]["path_old"].replace(store_url,""))
            path_new = os.path.normpath(edit_jsons[i]["path_new"].replace(store_url,""))
            path_new = path_new.replace("?","？")
            path_old = os.path.join(script_path,path_old)            
            path_new = os.path.join(script_path,path_new) 
            merged_list[path_old] = path_new

        for path_old in merged_list:
            path_new = merged_list[path_old]
            
            name_old = os.path.split(path_old)[-1]
            name_new = os.path.split(path_new)[-1]

            if os.path.isfile(path_old):
                print("%d : %s -> %s" % (i, name_old,name_new))
                os.rename(path_old, path_new)
            else:
                print("file not found : %s" % path_old)

# 重新生成目录

add_new = os.path.join(script_path,"add_new.py")
os.system("python %s" %add_new)
