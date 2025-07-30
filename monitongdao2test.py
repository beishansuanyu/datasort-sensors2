import struct
# -*- coding: utf-8 -*-

import tkinter as tk
from base64 import encode, decode
from os import truncate
from tkinter import filedialog
import os
import struct



root = tk.Tk()
root.withdraw()
f_path = filedialog.askopenfilename()

file = open(f_path, 'rb')
file_name = f_path.split('.')[0]
file_namelist = f_path.split('/')
long = len(file_namelist)
filename2 = file_namelist[long-1].split('.')[0]
file.seek(0, 2)
eof = file.tell()
file.seek(0, 0)
data = file.read()

datazhen_leng = 18  #单数据组长度
data_leng = 2

t_temp1 = 0
fs1 = 8000

t_temp2 = 0
fs2 = 20000

mlong = 0
data_temp = None

# f1 = open(file_name + "传感器1数据.txt", "w+")
# f2 = open(file_name + "模拟通道数据数据.txt", "w+")
f2 = open(filename2 + "模拟通道数据数据.txt", "w+")
data_leng = 2
# f0 = open("数字通道1数据.dat",'wb')
# f1 = open("数字通道2数据.dat",'wb')
# f2 = open("模拟通道数据数据.txt",'w+')
# f3 = open("传感器数据.txt",'w+')
# for i in range(16):
#     f.write('\t'+'通道'+str(i+1))
# f.write('\n')
# title =  '帧头' +'\t'+ '时标'+'\t'+ '状态字'+'\t'+ '滚转角'\
#         + '\t'+ '滚转角速度'+ '\t'+ '重力基准'+ '\t'+ 'ay'+ '\t'+ 'az'\
#         + '\t'+ 'Y轴加表采样值' + '\t'+ 'Z轴加表采样值' + '\t'+ 'ZLB_ang' \
#         + '\t' + 'HRG_ZT'+ '\t'+ 'HRG_rate' + '\t'+ 'HRG_angle' \
#         + '\t' + 'HRG_freq'+ '\t'+ 'HRG_fz' + '\t'+ 'HRG_zj' \
#         + '\t' + 'HRG_CNT'+ '\t'+ '温度' + '\t'+ '校验和'
# f1.write('时间' + '\t' + '通道1' + '\t' + '通道1' )
# f1.write('\n')

f2.write('时间' + '\t' + '通道1' + '\t' + '通道2'+ '\t' + '通道3'+ '\t' + '通道4'+ '\t' + '通道5'+ '\t' + '通道6'+ '\t' + '通道7'+ '\t' + '通道8')
xishu = [[0,1],
         [0,1],
         [0,1],
         [0,1],
         [0,1],
         [0,2.2],
         [0,2.2],
         [0,2.2]]



# def match_example1(item):
#     global t_temp1
#
#     pattern1 = b'\xEb\x90'
#     n = 0
#     while n < 2176:
#         t_temp = t_temp1
#         str1 = '\n' + str(t_temp)
#         f1.write(str1)
#         m = item.find(pattern1, n, 2176)
#         if m != -1 and m + 8 < 2184:
#             dat = int.from_bytes(item[m + 2:m + 4], byteorder='big', signed=True) / 65.5
#             str1 = '\t' + str(dat)
#             f1.write(str1)
#             dat = int.from_bytes(item[m + 4:m + 6], byteorder='big', signed=True) / 65.5
#             str1 = '\t' + str(dat)
#             f1.write(str1)
#             dat = int.from_bytes(item[m + 6:m + 8], byteorder='big', signed=True) / 65.5
#             str1 = '\t' + str(dat)
#             f1.write(str1)
#         else:
#             break
#         n = m + 8
#         t_temp1 = t_temp1 + 1 / fs1


def match_example3(item, data_temp1, rlong):
    ampliy_paramater = 2**15
    global t_temp2
    if rlong != 0:

        i2 = 0

        data_temp2 = data_temp1 + item[0:datazhen_leng - rlong]
        while i2 <8:
            m2 = i2*2
            data_temp3 = data_temp2[2+m2:2+m2+data_leng]
            dat = (int.from_bytes(data_temp2[2+m2:2+m2+data_leng], byteorder='big', signed=True) / ampliy_paramater*10 - xishu[i2][0])*xishu[i2][1]
            str1 = '\t' + str('{:.6f}'.format(dat))
            f2.write(str1)
            i2 = i2+1

        # dat = int.from_bytes(data_temp2[2+data_leng:2+data_leng*2], byteorder='big', signed=True) / ampliy_paramater
        # str1 = '\t' + str('{:.6f}'.format(dat))
        # f2.write(str1)

        t_temp2 = t_temp2 + 1 / fs2
    else:
        None

    pattern1 = b'\xEb'
    n = datazhen_leng-rlong
    while n < 2176:
        t_temp = t_temp2
        str1 = '\n' + str(t_temp)
        f2.write(str1)
        m = item.find(pattern1, n, 2176)
        if m != -1 and m + datazhen_leng < 2176:

            i3 = 0
            while i3 < 8:
                m3 = i3*2
                data_temp3 = item[m + 2+m3:m + 2+m3 + data_leng]
                dat = (int.from_bytes(item[m + 2+m3:m + 2+m3 + data_leng], byteorder='big', signed=True) / ampliy_paramater*10- xishu[i3][0])*xishu[i3][1]
                str1 = '\t' + str('{:.6f}'.format(dat))
                f2.write(str1)
                i3 = i3+1
            # dat = int.from_bytes(item[m+2:m+2+data_leng], byteorder='big', signed=True) /ampliy_paramater*5
            # str1 = '\t' + str( '{:.6f}'.format(dat))
            # f2.write(str1)
            # dat = int.from_bytes(item[m+2+data_leng:m+2+data_leng*2], byteorder='big', signed=True) / ampliy_paramater*11
            # str1 = '\t' + str( '{:.6f}'.format(dat))
            # f2.write(str1)

            mlong = 0
            data_temp = None
        elif m != -1 and m + datazhen_leng > 2176:
            mlong = 2176 - m
            data_temp = item[m:2176]
            break
        else:
            mlong = 0
            data_temp = None
            break
        n = m + datazhen_leng

        t_temp2 = t_temp2 + 1 / fs2
    return data_temp, mlong


# def match_example1(item):
#     pattern1 = b'\xEb\x90'
#     n=0
#     while n <2183:
#
#         m = item.find(pattern1, n, 2183)
#         if m != -1:
#             write1(item[m+2:m+11])
#             global t_temp1
#             t_temp1 += 1/fs_s
#         else:
#             break
#         n = m+9
#
# def match_example2(item):
#
#     pattern1 = b'\xEb\x90'
#     n=0
#     while n <2183:
#
#         m = item.find(pattern1, n, 2183)
#         if m != -1:
#             write1(item[m+2:m+11])
#             global t_temp1
#             t_temp1 += 1/fs_s
#         else:
#             break
#         n = m+9


pattern1 = b'\x1a\xcf\xfc\x1d'

n = 0
while n < eof:
    m = data.find(pattern1, n, eof)
    if m != -1 and m + 2184 < eof:
        channel = data[m + 6:m + 8]
        if channel == b'\x00\x10':
            data_temp, mlong = match_example3(data[m + 8:m + 2184], data_temp, mlong)
        else:
            pass

    else:
        break
    n = m + 2184

# f1.close()
f2.close()

print("helloworld")

# result = struct.unpack('format string', data)