#!/usr/bin/python
import re
import glob
import os

def sub(string):
    i = re.sub('^\x1b[[0-9;]*m.*\x1b\[m$', '', string, 0, re.MULTILINE)   
    i = re.sub('\x1b[[0-9;]*[mABCDHJKsu]', '', i)   
    i = re.sub(r'[作者|標題|時間].*\n', '', i)
    i = re.sub(r'^[─|※|:].*$\n', '', i)
    i = re.sub(r'瀏覽.*離開', '', i)
    i = re.sub(r'[→|推|噓].*[:][ ]', '', i)
    i = re.sub(r'[0-9]*/[0-9]*[ ]*[0-9]*:[0-9]*$', '', i)
    i = re.sub(r'[--]', '', i)
    i = re.sub(r'[ ]*[A-Za-z0-9/:.…_?=]*[ ]*', '', i)
    i = re.sub(r'^[ ]*|[ ]*$|', '', i)
    i = re.sub(r'[●■□▲「」％：【】~()（）%"『』〔〕《》[]]*', '', i)
    i = re.sub(r'[，、。？！；／▲「」％：【】~()（）%"『』〔〕?!,.]*$|^[，、。？！；／▲「」％：【】~()（）%"『』〔〕?!,.]*', '', i)
    i = re.sub(r'[，、。？！；／?!,.][ ]*|[ ]+', '\n', i)
    i = re.sub(r'^$\n', '', i)
    return i

for _file in glob.glob("./article/*.in"):
    fi = open(_file, "r")
    output_name = re.sub('in$', 'out', _file)
    fo = open(output_name, "w")

    for line in fi:
        fo.write(sub(line))

    fi.close()
    fo.close()
