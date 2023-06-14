# 后院仓库
存放一些东西，没什么好看的，去[前端](https://github.com/umas2022/backyard_lite)


### 环境初始化
- 只有一个python库
```
pip install pinyin
```


### 新增内容
- 目前支持的格式: ["jpg", "gif", "jpeg", "png", "webp", "mp4"]
- 新增的沙雕图、表情包、视频分别放在./new_image/、./new_sticker/、./new_video/文件夹下，然后运行./add_new.py，新增内容将以序号重命名并移动至./storage/对应目录，同时自动更新./index/文件夹下索引json
- 可以将文件夹整个放进./new_*目录，脚本将遍历所有子级（但是移动之后剩下的空文件夹不能自动删除（有空再做））


### 修改tag
- 网页修改完成后点击【导出修改】按钮，将生成的edit.json文件放在./edit_tag/文件夹下，然后运行./edit_tag.py
- 注意最好不要使用单个英文字母作为tag, 单个大写字母作为tag分隔符使用,在前端会显示成蓝色不可点击


### 辅助功能
- 资源查重
  - 有空做
- 搜索相似图片
  - 没啥想法
- 图片压缩
  - 待会去pctools里面拷一份过来
- 视频压缩
  - 待会去pctools里面拷一份过来
- 批量加幻影坦克（仅黑白）
  - 待会去pctools里面拷一份过来
- 视频转gif
  - 待会去pctools里面拷一份过来


### 关于后院
- GitHub居然不限容量，笑死，直接拿来当图床
- 