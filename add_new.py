'''
两次push之间最好间隔30分钟以上,否则workflow可能会覆盖
https://github.com/umas2022/umas2022.github.io/actions

'''

import os
import json
from pinyin import pinyin  # pip install pinyin
import shutil
import subprocess
import datetime


import sys
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)


# 合法目标资源类型
legal_type = ["jpg", "gif", "jpeg", "png", "webp", "mp4"]

# 现存资源路径
path_image = os.path.normpath(os.path.join(script_path, "storage/image"))
path_sticker = os.path.normpath(os.path.join(script_path, "storage/sticker"))
path_video = os.path.normpath(os.path.join(script_path, "storage/video"))

# 新增资源路径
path_new_image = os.path.join(script_path, "new_image")
path_new_sticker = os.path.join(script_path, "new_sticker")
path_new_video = os.path.join(script_path, "new_video")

# 索引json路径
json_image = os.path.normpath(os.path.join(script_path, "index/list_image.json"))
json_sticker = os.path.normpath(os.path.join(script_path, "index/list_sticker.json"))
json_video = os.path.normpath(os.path.join(script_path, "index/list_video.json"))
json_tag = os.path.normpath(os.path.join(script_path, "index/list_tag.json"))

# 更新记录路径
update_json = os.path.normpath(os.path.join(script_path, "index/list_update.json"))


def get_first_dir(path_in):
    '''一级文件夹遍历'''
    for dir in os.listdir(path_in):
        full_path = os.path.normpath(os.path.join(path_in, dir))
        if os.path.isdir(full_path):
            yield dir


def get_file(path_in):
    '''所有层级文件遍历'''
    for root, dirs, files in os.walk(path_in):
        for fileName in files:
            if fileName == ".gitkeep":
                continue
            full_path = os.path.normpath(os.path.join(root, fileName))
            yield full_path


def add_new(path_store, path_new):
    '''添加新的图片(重命名并移动至相应pack)'''
    pack_list = [x for x in get_first_dir(path_store)]

    pack_last_num = int(pack_list[-1].replace("pack", ""))
    img_list = [x for x in get_file(path_store + "/" + pack_list[-1])]
    if img_list == []:
        img_last_num = 0
    else:
        img_last_name = os.path.split(img_list[-1])[-1]
        img_last_num = int(img_last_name[0:4])

    def rename_num(methodPathIn: str, num: int):
        '''处理方法: 四位数字序号命名'''
        dir, name = os.path.split(methodPathIn)
        fileFormat = name.split(".")[-1]
        name_new = str(num).zfill(4) + "." + fileFormat
        methodPathOut = os.path.join(dir, name_new)
        return os.path.normpath(methodPathOut)

    def sort_path(path_in: str):
        '''拼接输出路径'''
        dir, name = os.path.split(path_in)
        group = dir.replace("new_", "")
        img_num = int(name.replace("pack", "").split(".")[0])
        pack_num = (img_num - 1) // 50 + 1
        path_dir = os.path.normpath(path_store + "/pack" + str(pack_num).zfill(4))
        if not os.path.isdir(path_dir):
            os.mkdir(path_dir)
        path_file = path_dir + "/" + name
        return path_file

    # 重命名并移动新图片
    for img_path in get_file(path_new):
        img_last_num += 1
        img_path_new = rename_num(img_path, img_last_num)
        os.rename(img_path, img_path_new)
        shutil.move(img_path_new, sort_path(img_path_new))
        print("add_new : %s" % sort_path(img_path_new))

    return img_last_num


def list_update(path_store, list_json):
    '''更新json索引(./index/list_xxx.json)'''
    img_list = {}
    tag_list = []

    def get_tag_list(name: str):
        '''文件名拆分tag'''
        suffix = name.split(".")[-1]
        name = name.replace("." + suffix, "")
        return name.split("_")[1:]

    with open(list_json, 'w', encoding="utf-8") as file:
        for pack in get_first_dir(path_store):
            img_list[pack] = []
            print("list_updata : %s - %s" % (path_store, pack))
            for full_path in get_file(os.path.join(path_store, pack)):
                image = os.path.split(full_path)[-1]
                if not str(image).split(".")[-1] in legal_type:
                    print("error : illegal type !")
                    continue
                img_list[pack].append(image)
                tag_list = list(set(tag_list) | set(get_tag_list(image)))
        js_str = json.dumps(img_list, ensure_ascii=False)
        file.write(js_str)
    return tag_list


def tag_update(tag_list: list):
    '''更新tag列表(./index/list_tag.json)'''
    with open(json_tag, 'w', encoding="utf-8") as file:
        js_str = json.dumps(tag_list, ensure_ascii=False)
        file.write(js_str)


def record_update(img_num, stk_num, vid_num):
    '''更新记录列表(.index/list_update.json)'''
    now = datetime.datetime.now()  # 获取当前时间
    formatted_date = now.strftime("%Y.%m.%d")  # 将时间格式化为2023.4.19的格式
    new_rec = str(formatted_date) + ": "

    def find_last(json, tag, start) -> str:
        '''返回上次更新的序号'''
        img_index1 = json[start].find(tag) + 3
        if img_index1 == 2:
            return find_last(json, tag, start + 1)
        img_index2 = json[start].find(",", img_index1)
        if img_index2 == -1:
            img_index2 = len(json[start])
        img_last = json[start][img_index1:img_index2]
        return img_last

    with open(update_json, 'r+', encoding="utf-8") as file:
        record = json.load(file)
        img_last = int(find_last(record, "img", 0))
        stk_last = int(find_last(record, "stk", 0))
        vid_last = int(find_last(record, "vid", 0))
        new_rec+="img"+str(img_num)+", " if not img_last == img_num else ""
        new_rec+="stk"+str(stk_num)+", "  if not stk_last == stk_num else ""
        new_rec+="vid"+str(vid_num)+", "  if not vid_last == vid_num else ""
        new_rec = new_rec.strip(" ").strip(",")
        if not new_rec == formatted_date+":":
            record = [new_rec] + record
            js_str = json.dumps(record, ensure_ascii=False,indent='\t')
            file.seek(0) 
            file.truncate()
            file.write(js_str)

# 添加新资源
img_num = add_new(path_image, path_new_image)
stk_num = add_new(path_sticker, path_new_sticker)
vid_num = add_new(path_video, path_new_video)


# 更新资源列表
tag_list_img = list_update(path_image, json_image)
tag_list_stk = list_update(path_sticker, json_sticker)
tag_list_vid = list_update(path_video, json_video)


# 更新tag列表（仅表情包）
# tag_list = list(set(tag_list_img) | set(tag_list_stk) | set(tag_list_vid))
tag_list = tag_list_stk
sorted_lst = sorted(tag_list, key=lambda x: pinyin.get(x, format='strip'))
tag_update(sorted_lst)


# 更新记录列表
record_update(img_num, stk_num, vid_num)


# 上传
# print("\n===== push source =====\n")
# subprocess.run(["git", "add", "."], cwd=".", shell=True)
# subprocess.run(["git", "commit", "-m", "add pack"], cwd=".", shell=True)
# subprocess.run(["git", "push"], cwd=".", shell=True)
