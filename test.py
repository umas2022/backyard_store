import pinyin


sep = [chr(char) for char in range(ord('A'), ord('Z')+1)]

tag = ["啊", "111","把","AAABBB"]

tag +=sep

sorted_tags = sorted(tag, key=lambda x: pinyin.get(x))
print(sorted_tags)

