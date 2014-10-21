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

os.chdir("./article")

for file in glob.glob("*.in"):
    fi = open(file, "r")
    fo = open(file+".out", "w")

    for line in fi:
        fo.write(sub(line))

    fi.close()
    fo.close()
