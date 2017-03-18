#coding=utf-8

import os
import sys
import os.path
import codecs
import chardet

def walkDirectory(rootPath, f, ext_filters):
    for dir, _, files in os.walk(rootPath):
        for filename in files:
            _, ext = os.path.splitext(filename)
            if ext in ext_filters:
                f(os.path.join(dir, filename))

def processFunc(fileName):
    encodingPredict = chardet.detect(open(fileName, "r").read())
    
    if encodingPredict['confidence'] >= 0.9:
        if encodingPredict['encoding'].find("GB") != -1:
            print "processing", fileName
            fo = codecs.open(fileName, "r", encoding = "GB18030")
            content = fo.read()
            fo.close()
            fw = codecs.open(fileName, "w", encoding = "utf-8")
            fw.write(content)
            fw.close()            
        else:
            print "Skip", encodingPredict, fileName
    else:
        print "Can`t decide encoding", encodingPredict, fileName
        

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: python EncodingConverter.py path"
    else:
        walkDirectory(sys.argv[1], processFunc, [".cpp", ".h"])
    