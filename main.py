import struct
# -*- coding: utf-8 -*-

import tkinter as tk
from base64 import encode, decode
from tkinter import filedialog
import os
import struct



root = tk.Tk()
root.withdraw()
f_path = filedialog.askopenfilename()




file = open(f_path, 'rb')
file_name =f_path.split('.')[0]
file.seek(0,2)
eof = file.tell()
file.seek(0,0)
data = file.read()
t_temp1 = 0
fs1 = 8000

t_temp2 = 0
fs2 = 4000

mlong = 0
data_temp = None



f1 = open(file_name+"传感器1数据.txt", "w+")
f2 = open(file_name+"传感器2数据.txt", "w+")
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
f1.write(  '时间'+  '\t' + 'X轴(°/s）'+'\t'+ 'Y轴(°/s）'+ '\t'+ 'Z轴(°/s）'  )
# f1.write('\n')

f2.write( '时间'+  '\t' + 'X轴（g）'+'\t'+ 'Y轴（g）'+ '\t'+ 'Z轴（g）' )










def match_example1(item):
    global t_temp1

    pattern1 = b'\xEb\x90'
    n=0
    while n <2176:
        t_temp = t_temp1
        str1 = '\n' + str(t_temp)
        f1.write(str1)
        m = item.find(pattern1, n, 2176)
        if m != -1 and m+8<2184:
            dat = int.from_bytes(item[m+2:m+4], byteorder='big', signed=True)/65.5
            str1 = '\t' + str(dat)
            f1.write(str1)
            dat = int.from_bytes(item[m+4:m+6], byteorder='big', signed=True)/65.5
            str1 = '\t' + str(dat)
            f1.write(str1)
            dat = int.from_bytes(item[m+6:m+8], byteorder='big', signed=True)/65.5
            str1 = '\t' + str(dat)
            f1.write(str1)
        else:
            break
        n = m+8
        t_temp1 = t_temp1 + 1/fs1

def match_example2(item,data_temp1,rlong):
    ampliy_paramater = 51200*16
    global t_temp2
    if rlong !=0:

        data_temp2 = data_temp1 + item[0:11-rlong]
        dat = int.from_bytes(data_temp2[2:5], byteorder='big', signed=True) /ampliy_paramater
        str1 = '\t' + str(dat)
        f2.write(str1)
        dat = int.from_bytes(data_temp2[5:8], byteorder='big', signed=True) / ampliy_paramater
        str1 = '\t' + str(dat)
        f2.write(str1)
        dat = int.from_bytes(data_temp2[8:11], byteorder='big', signed=True) / ampliy_paramater
        str1 = '\t' + str(dat)
        f2.write(str1)
        t_temp2 = t_temp2 + 1/fs2
    else:
        None

    pattern1 = b'\xEb'
    n=0
    while n <2176:
        t_temp = t_temp2
        str1 = '\n' + str(t_temp)
        f2.write(str1)
        m = item.find(pattern1, n, 2176)
        if m != -1 and m+11<2176:
            dat = int.from_bytes(item[m+2:m+5], byteorder='big', signed=True)/ampliy_paramater
            str1 = '\t' + str(dat)
            f2.write(str1)
            dat = int.from_bytes(item[m+5:m+8], byteorder='big', signed=True)/ampliy_paramater
            str1 = '\t' + str(dat)
            f2.write(str1)
            dat = int.from_bytes(item[m+8:m+11], byteorder='big', signed=True)/ampliy_paramater
            str1 = '\t' + str(dat)
            f2.write(str1)
            mlong = 0
            data_temp = None
        elif m != -1 and m+11>2176:
            mlong = 2176-m
            data_temp = item[m:2176]
            break
        else:

            mlong = 0
            data_temp = None
        n = m+11

        t_temp2 = t_temp2 + 1/fs2
    return data_temp,mlong

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
while n <eof:
    m = data.find(pattern1,n,eof)
    if m != -1 and m+2184<eof:
        channel = data[m+4:m+6]
        if channel == b'\x66\x66':
             match_example1(data[m+8:m+2184])
        elif channel == b'\x55\x55':
             data_temp,mlong = match_example2(data[m + 8:m + 2184],data_temp,mlong)
        else:
            None




    else:
        break
    n = m+2184



f1.close()
f2.close()



print("helloworld")

# result = struct.unpack('format string', data)