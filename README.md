# 后院仓库
存放一些东西，没什么好看的，去主页[（链接）](https://umas2022.github.io)


### 环境初始化
- 两个python库
```
# 生成tag
pip install pinyin
# 图片去重
pip install imagehash
```


### 新增内容(add_new.py)
- 目前支持的格式: ["jpg", "gif", "jpeg", "png", "webp", "mp4"]
- 新增的沙雕图、表情包、视频分别放在./new_image/、./new_sticker/、./new_video/文件夹下，然后运行./add_new.py，新增内容将以序号重命名并移动至./storage/对应目录，同时自动更新./index/文件夹下索引json
- 可以将文件夹整个放进./new_*目录，脚本将遍历所有子级（但是移动之后剩下的空文件夹不能自动删除（有空再做））


### 修改tag(edit_tag.py)
- 网页修改完成后点击右上角【导出修改】按钮，将生成的edit.json文件放在./edit_tag/文件夹下，然后运行./edit_tag.py
- 注意最好不要使用单个英文字母作为tag, 单个大写字母作为tag分隔符使用,在前端会显示成橙色不可点击


### 图片去重(duplicate_rm.py)
- 脚本已经转移到电脑配件继续开发



### 重新排序(re_index.py)
- 这个方法还没做
- 删除图片后重新排序
- 删除后不重新排序也不会引起任何报错, 但序号不连续会引起强迫症患者血压升高
- 另外发现有一些序号莫名其妙重复了, 这种情况也需要考虑




### 关于后院
- GitHub居然不限容量，笑死，直接拿来当图床
