__author__ = 'oier'

import os
import numpy as np
from data.parameters import true_params
from data.parameters import false_params
import distance as dist
import numpy as np

def pdftotext(path):
    os.system("pdftotext {data}".format(data=path))
    return(path.replace(".pdf",".txt"))

import pandas as pd
def parse(path):
    txt = pd.read_table(path, sep='\n', na_values=False, header=None)

    for i in txt.index:
        try :
            if pd.isnull(float(txt.ix[i])) == False:
                name = getname(i,txt)
                print(name)
                print(float(txt.ix[i]))
        except :
            pass

def getname(index, df):
    name = ""
    for i in range(0,index):
        size = len(df.ix[i].to_string().split())
        idxname =  " ".join(df.ix[i].to_string().split()[1:size])
        if (len( idxname )> 5) and idxname != None and idxname != "NaN":
            name = idxname
            #print(name)
    return (name)

from collections import deque

def getnamedict(path):
    dict = {}
    numdict = {}
    names = deque()
    txt = pd.read_table(path, sep='\n', na_values=False, header=None)
    name = ""
    for i in txt.index:
        try :
            size = len(txt.ix[i].to_string().split())
            nextname =  " ".join(txt.ix[i].to_string().split()[1:size])
            if (len( nextname )> 5) and \
                            nextname != None and \
                            nextname != "NaN" and \
                    isclean(nextname) and \
                    validateparam(nextname):
                names.append(nextname)
                dict[i] = nextname
                #print(name)
                #print(nextname)
            if pd.isnull(float(txt.ix[i])) == False:
                number = float(txt.ix[i])
                numdict[names.pop()] = number
                #print(number)
                #print(i)
        except :
            pass

    print(dict.keys())
    print(dict.values())
    print(numdict.keys())
    print(numdict.values())

    #organize(dict,numdict)
    #    print(dict[i])

def organize(names, numbers):
    '''
    :param names: must be dictionary
    :param numbers: must be dictionary
    :return: dictionary, dict[name] = number
    '''

    numbs = dict(numbers)
    nams = dict(names)

    conn1 = {}
    conn2 = {}
    array1 = np.array(nams.keys())


    for i in numbs.keys():
        actual = 100.0
        inconn2 = False

        key = min(nams.keys(), key=lambda k: abs(k - i))
        print(" {} - {} ".format(key,i))
        print(" {} - {} ".format(nams[key],numbs[i]))



        '''
        for j in numbs.keys():
            actual = i - j
            if ( actual > conn1[i] or conn1[i] == None):
                if( conn2[j] == None):
                    conn1[i] = j
                    conn2[j] = actual
                else:
                    best = j
                    inconn2 = True
            else if (conn2[j] != None ):
            '''

    return()

def isclean(word):
    w = str(word)
    test = True
    strg = "_[]*"
    bool = True
    for i in range(len(strg)):
        c = strg[i]
        bool = bool or (w.find(c) != -1)
    test = test and (bool)
    return(test)




def validateparam(word):
    t_dist = []
    f_dist = []

    for i in true_params:
        t_dist.append(dist.levenshtein(word,i))
    for i in false_params:
        f_dist.append(dist.levenshtein(word, i))

    print("Word: {}, T: {} , F: {}".format(word, np.min(t_dist), np.min(f_dist[0])))

    if( min(t_dist) == 0):
        print("TRUE")
        return (True)
    if (min(f_dist) == 0):
        print("FALSE")
        return("FALSE")
    if ( np.mean(t_dist )< np.mean(f_dist) ):
        print("TRUE")
        return(True)
    print("FALSE")
    return(False)

def getmyarray(path, apath):
    dict = {}
    appearances = {}
    names = deque()
    with open(path) as f:
        txt = f.readlines()
    #txt = pd.read_table(path, sep='\n', na_values=False, header=None)
    array_txt = pd.read_table(apath, sep='\n', header=None)
    name = ""
    for i in txt:
        actual = i.replace("\n", '')
        if(len(actual.strip()) == 0):
            continue
        try :
            number = float(actual)

            if (number > 10000000):
                continue
            try:
                appearances[actual] += 1
            except:
                appearances[actual] = 1

            name = localgetmyarray(path, apath, actual, appearances[i])
            dict[name] = i
            print("name: {} numb: {}".format(name, i))

        except :
            pass

    print(dict.keys())
    print(dict.values())


def localgetmyarray(path, apath, word, count):

    with open(path) as f:
        txt = f.readlines()
    #txt = pd.read_table(path, sep='\n', na_values=False, header=None)
    f = open(apath)
    array_txt_str = f.read()
    name = ""
    idx = [k.start() for k in re.finditer(word, array_txt_str)][count -1]

    opt = len(array_txt_str)

    apps ={}

    for i in txt:
        try :
            nextname =  i.replace("\n", '')
            try :
                float(nextname)
            except :
                if (len( nextname )> 5) and nextname != None and \
                            nextname != "NaN" and isclean(nextname):
                    try:
                        apps[nextname ] += 1
                    except:
                        apps[nextname] = 1

                    id = [k for k in re.finditer(nextname, array_txt_str)][apps[nextname]-1].start()
                    myopt = idx - id
                    if (myopt > 0) and (myopt < opt):
                        opt = myopt
                        name = nextname
        except :
            pass

    print("optimum: {} number: {} found: {}".format(opt, word, name))
    f.close()
    return name


#DOWN FROM HERE JAVA+PYTHON PDF TO TEXT:
import re
import extractText as txt

def remove_unwanted(str):
    s = re.sub(r'\[.*?\]', '',str)
    s = s.replace("\*", "")
    s = s.replace("\n", "")
    return (s)

def line_control(str):
    #may return True if str is not valid
    #returns false if str is valid
    if(len(str) < 15):
        return True
    if(len(str) == 1):
        return True
    if(len(str.split(" ")) > 10):
        return True
    return False

def line_parser(str):
    item = ''
    valor = ''
    dict = {}
    sline = str.split(" ")
    helper = {}
    pos = 0
    for schar in sline:
        try:
            #dict["val"]
            if(len(dict.keys()) == 3 and len(sline) > 6):
                helper[pos] = dict
                dict = {}
                pos += 1
            dict["val"] #to force failure/raise ofd exception
        except:
            try:
                valor = ''
                table = [char for char in schar if '/' in char]
                if schar.find('%') != -1:
                    valor = schar
                if len(table) > 0:
                    valor = schar
                if(valor != ''):
                    dict["val"] = valor
                    continue
            except:
                pass
        try:
            #dict["num"]
            if(len(dict.keys()) == 3 and len(sline) > 6):
                helper[pos] = dict
                dict = {}
                pos += 1
            dict["num"]
        except:
            try:
                num = float(schar)
                if(num > 10000):
                    return({})
                dict["num"] = num
                continue
            except:
                pass

        try:
            dict["item"] += " " + schar
        except:
            dict["item"] = schar

    helper[pos] = dict
    return(helper)


def getfromjava(path, dest=''):

    if (dest == ''):
        d = path.replace(".pdf", ".txt")
    txt.extractText(path, d, '')

    with open(d) as f:
        text = f.readlines()

    for line in text:
        sline = remove_unwanted(line)
        if(line_control(sline) == True):
            continue
        dict = line_parser(sline)
        for i in dict.keys():
            if(len(dict[i].keys()) == 3):
                print("ITEM: {} NUM: {} VAL: {}".format(dict[i]["item"], dict[i]["num"], dict[i]["val"]))

