# coding:utf-8
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import os
import cv2
import PIL.Image as PImage
from PIL import ImageFont, ImageDraw
import numpy as np
import random
from dictionary import alphabet, nations
from address_set import province_set, city_set, couty_set


try:
    from Tkinter import *
    from ttk import *
    from tkFileDialog import *
    from tkMessageBox import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter.filedialog import *
    from tkinter.messagebox import *


if getattr(sys, 'frozen', None):
    base_dir = os.path.join(sys._MEIPASS, 'usedres')
else:
    base_dir = os.path.join(os.path.dirname(__file__), 'usedres')

def changeBackground(img, img_back, zoom_size, center):
    # 缩放
    img = cv2.resize(img, zoom_size)
    rows, cols, channels = img.shape

    # 转换hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 获取mask
    #lower_blue = np.array([78, 43, 46])
    #upper_blue = np.array([110, 255, 255])
    diff = [5, 30, 30]
    gb = hsv[0, 0]
    lower_blue = np.array(gb - diff)
    upper_blue = np.array(gb + diff)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('Mask', mask)

    # 腐蚀膨胀
    erode = cv2.erode(mask, None, iterations=1)
    dilate = cv2.dilate(erode, None, iterations=1)

    # 粘贴
    for i in range(rows):
        for j in range(cols):
            if dilate[i, j] == 0:  # 0代表黑色的点
                img_back[center[0] + i, center[1] + j] = img[i, j]  # 此处替换颜色，为BGR通道

    return img_back

def paste(avatar, bg, zoom_size, center):
    avatar = cv2.resize(avatar, zoom_size)
    rows, cols, channels = avatar.shape
    for i in range(rows):
        for j in range(cols):
            bg[center[0] + i, center[1] + j] = avatar[i, j]
    return bg

def generator_v2(name,
                 sex,
                 nation,
                 year,
                 mon,
                 day,
                 org, life, addr, idn, fname):
    global ename, esex, enation, eyear, emon, eday, eaddr, eidn, eorg, elife, ebgvar

    im = PImage.open(os.path.join(base_dir, 'empty.png'))
    avatar = cv2.imread(fname)  # 500x670

    name_font = ImageFont.truetype(os.path.join(base_dir, 'hei.ttf'), 72)
    other_font = ImageFont.truetype(os.path.join(base_dir, 'hei.ttf'), 60)
    bdate_font = ImageFont.truetype(os.path.join(base_dir, 'fzhei.ttf'), 60)
    id_font = ImageFont.truetype(os.path.join(base_dir, 'ocrb10bt.ttf'), 72)

    draw = ImageDraw.Draw(im)
    draw.text((630, 690), name, fill=(0, 0, 0), font=name_font)
    draw.text((630, 840), sex, fill=(0, 0, 0), font=other_font)
    draw.text((1030, 840), nation, fill=(0, 0, 0), font=other_font)
    draw.text((630, 980), year, fill=(0, 0, 0), font=bdate_font)
    draw.text((950, 980), mon, fill=(0, 0, 0), font=bdate_font)
    draw.text((1150, 980), day, fill=(0, 0, 0), font=bdate_font)
    start = 0
    loc = 1120
    while start + 11 < len(addr):
        draw.text((630, loc), addr[start:start + 11], fill=(0, 0, 0), font=other_font)
        start += 11
        loc += 100
    draw.text((630, loc), addr[start:], fill=(0, 0, 0), font=other_font)
    draw.text((950, 1475), idn, fill=(0, 0, 0), font=id_font)
    draw.text((1050, 2750), org, fill=(0, 0, 0), font=other_font)
    draw.text((1050, 2895), life, fill=(0, 0, 0), font=other_font)

    ebgvar = True
    if ebgvar:
        avatar = cv2.cvtColor(np.asarray(avatar), cv2.COLOR_RGBA2BGRA)
        im = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGBA2BGRA)
        im = changeBackground(avatar, im, (500, 670), (690, 1500))
        im = PImage.fromarray(cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA))
    else:
        avatar = avatar.resize((500, 670))
        avatar = avatar.convert('RGBA')
        im.paste(avatar, (1500, 690), mask=avatar)

    return im


def IDcard_generator(amount):
    name_all = []
    sex_all = []
    nation_all = []
    addr_all = []
    year_all = []
    mon_all = []
    day_all = []
    id_all = []
    others = []

    numbers = '0123456789'

    for i in range(amount):

        name_length = random.randint(2, 4)
        result = random.sample(alphabet, name_length)
        name_all.append(''.join(result))

        result = random.sample(u'男女', 1)
        sex_all.append(''.join(result))

        result = random.sample(nations, 1)
        nation_all.append(''.join(result))

        result = random.sample(numbers, 4)
        year_all.append(''.join(result))

        result = random.sample(numbers, 2)
        mon_all.append(''.join(result))

        result = random.sample(numbers, 2)
        day_all.append(''.join(result))

        id = []
        addr = []
        province = random.sample(province_set, 1)[0]
        # province = [u'天津市', 12]
        addr += province[0]
        if province[0] in city_set.keys():
            city = random.sample(city_set[province[0]], 1)[0]
            addr += city[0]
            if city[0][0] in couty_set.keys():
                couty = random.sample(couty_set[city[0]], 1)
                addr += couty[0]
                id += str(couty[1])
            else:
                id += str(city[1])
                if len(id) == 4:
                    id += random.sample(numbers, 2)
        else:
            id += str(province[1])
            if len(id) == 2:
                id += random.sample(numbers, 4)
        addr = ''.join(addr)
        if len(addr) < 11:
            result = random.sample(alphabet, 11-len(addr))
            addr += ''.join(result)
        elif len(addr) > 11:
            addr = addr[:12]
        id += year_all[i]
        id += mon_all[i]
        id += day_all[i]
        id += random.sample(numbers, 3)
        id += random.sample(u'0123456789X', 1)
        addr_all.append(''.join(addr))
        id_all.append(''.join(id))

    return name_all, sex_all, nation_all, year_all, mon_all, day_all, addr_all, id_all


def tostr(a):
    return  ''.join(a)


if __name__ == '__main__':
    global ename, esex, enation, eyear, emon, eday, eaddr, eidn
    fragment_IDcard = True
    sample_sum = 1
    loop_num = 10
    for i in range(loop_num):
        ename, esex, enation, eyear, emon, eday, eaddr, eidn = IDcard_generator(sample_sum)
        avater_path = r'./avater/'+str(random.randint(1, 3))+'.png'
        img = generator_v2(tostr(ename),tostr(esex),tostr(enation),tostr(eyear),tostr(emon),tostr(eday),'江苏省徐州市铜山区派出所','2015.06.29-2025.06.29',tostr(eaddr),tostr(eidn),avater_path)
        region = img.crop([0,  img.size[1] /8, img.size[0], img.size[1] * 2 / 4])
        name = r'./fake_back/fake_back_'+str(i)+'.png'
        region.save(name)




