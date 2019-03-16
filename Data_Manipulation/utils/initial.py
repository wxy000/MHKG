# -*- coding: utf-8 -*-
import pinyin


# 输入name
def get_pinyin_first_alpha(name):
    return "".join([i[0] for i in pinyin.get(name, " ").split(" ")])


if __name__ == '__main__':
    data = get_pinyin_first_alpha("我不好")
    print(data)
