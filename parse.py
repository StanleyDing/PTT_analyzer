#!/usr/bin/python
import re
import glob
import os

def sub(string):
    # remove header
    i = re.sub('\x1b\[34;47m[ ](作者|標題|時間).*\n', '', string)
    # remove trailer
    i = re.sub(r'^.*瀏覽.*目前顯示.*離開.*$', '', i, 0, re.MULTILINE)
    # reply
    i = re.sub('^\x1b\[1;3.m[→|推|噓].*?[:][ ]*', '', i, 0, re.MULTILINE)
    # control code
    i = re.sub('\x1b\[[0-9;]*[mABCDHJKsu]', '', i)   
    # quote, system info, etc.
    i = re.sub(r'^[─|※|:].*', '', i, 0, re.MULTILINE)
    # signature
    i = re.sub('^--.*--$', '', i, 0, re.MULTILINE | re.DOTALL)
    # alphabet
    i = re.sub('[A-Za-zＡ-Ｚ]+', ' ', i)
    # numbers
    i = re.sub('[0-9]+', ' ', i)
    i = re.sub('[１２３４５６７８９０]+', ' ', i)
    # punctuations
    i = re.sub('[!@#$%^&*()_+-=,\./;\'\[\]\\<>\?:"{}|`~]+', ' ', i)
    i = re.sub('[，。　、！？⋯；：]+', ' ', i)
    i = re.sub('[「」【】（）『』〔〕《》]+', ' ', i)
    i = re.sub('[％＋＝－＊／＼＃＄＆]+', ' ', i)
    i = re.sub('[╱“”∼─]+', ' ', i)
    # shapes
    i = re.sub('[●•○■□▲]+', ' ', i)
    # spaces
    i = re.sub('\s+', '\n', i)
    # blank lines
    i = re.sub('^\s+', '', i, 0, re.MULTILINE)
    return i

for _file in glob.glob("./article/*.in"):
    fi = open(_file, "r")
    output_name = re.sub('in$', 'out', _file)
    fo = open(output_name, "w")

    x = fi.read()
    fo.write(sub(x))

    fo.close()
    fi.close()
