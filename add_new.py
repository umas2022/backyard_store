'''
两次push之间最好间隔30分钟以上,否则workflow可能会覆盖
https://github.com/umas2022/umas2022.github.io/actions

'''

import os
import json
from pinyin import pinyin  # pip install pinyin
import shutil
import subprocess

import sys
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)


# 合法目标资源类型
legal_type = ["jpg", "gif", "jpeg", "png", "webp","mp4"]

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
            full_path = os.path.normpath(os.path.join(root, fileName))
            yield full_path




def add_new(path_store,path_new):
    '''添加新的图片'''
    pack_list = [x for x in get_first_dir(path_store)]
    
    pack_last_num = int(pack_list[-1].replace("pack", ""))
    img_list = [x for x in get_file(path_store + "/" + pack_list[-1])]
    if img_list ==[]:
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
        print("add_new : %s"% sort_path(img_path_new))





def list_update(path_store, list_json):
    '''更新json索引'''
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
                if not str(image).split(".")[-1] in legal_type :
                    print("error : illegal type !")
                    continue
                img_list[pack].append(image)
                tag_list = list(set(tag_list) | set(get_tag_list(image)))
        js_str = json.dumps(img_list, ensure_ascii=False)
        file.write(js_str)
    return tag_list




def tag_update(tag_list: list):
    '''更新tag列表'''
    with open(json_tag, 'w', encoding="utf-8") as file:
        js_str = json.dumps(tag_list, ensure_ascii=False)
        file.write(js_str)





# 添加新图片
add_new(path_image,path_new_image)
add_new(path_sticker,path_new_sticker)
add_new(path_video,path_new_video)


# 更新图片列表
tag_list_img = list_update(path_image,json_image)
tag_list_stk = list_update(path_sticker,json_sticker)
tag_list_vid = list_update(path_video,json_video)


# 更新tag列表（仅表情包）
# tag_list = list(set(tag_list_img) | set(tag_list_stk) | set(tag_list_vid))
tag_list = tag_list_stk
sorted_lst = sorted(tag_list, key=lambda x: pinyin.get(x, format='strip'))
tag_update(sorted_lst)



# 上传
# print("\n===== push source =====\n")
# subprocess.run(["git", "add", "."], cwd=".", shell=True)
# subprocess.run(["git", "commit", "-m", "add pack"], cwd=".", shell=True)
# subprocess.run(["git", "push"], cwd=".", shell=True)
