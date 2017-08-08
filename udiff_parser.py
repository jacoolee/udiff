#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Tue Aug  8 19:37:21 2017
# ht <515563130@qq.com, weixin:jacoolee>

import re, json

difflines=[
    '--- 1	Tue Aug  8 18:46:30 2017',
    '+++ 2	Tue Aug  8 18:51:42 2017',
    '@@ -1,0 +2 @@',
    '+* unified:  highlights clusters of changes in an inline format.',
    '@@ -3,2 +4 @@',
    '-Simple is better than complex.',
    '-Complex is better than complicated.',
    '+xComplex is better than complicated.',
    '@@ -6 +6,3 @@',
    '-Sparse is better than dense.',
    '+Sparse lists every line and',
    '+highlights interline changes',
    '+is better than dense.',
]

def parseChuck(chuckline):
    return [int(i or 1) for i in re.compile('-(\d+),?(\d+)* \+(\d+),?(\d+)*').findall(chuckline)[0]]

def getDiffMap(difflines, enable_check=True):

    # first do parse simple logic
    s1, c1, s2, c2,lmax, rmax = None, None, None, None, None, None

    line2diffmap = {}

    if enable_check:
        difflines.append('@@')

    for l in difflines:
        if l.startswith('---'):
            continue
        elif l.startswith('+++'):
            continue
        elif l.startswith('@@'):

            if enable_check:
                if lmax != None:
                    print 'parse left ok?', s1==lmax, 'parse right ok?', s2==rmax, '\n'
                if l=='@@':
                    return line2diffmap

            # parse chunk
            s1, c1, s2, c2 = parseChuck(l)
            print s1,c1,s2,c2, 'chuck =', l

            if enable_check:
                lmax, rmax = s1+c1, s2+c2


        elif l.startswith('-'):
            if s1 in line2diffmap:
                line2diffmap[s1][1] = l[1:]
            else:
                line2diffmap[s1] = [s1, l[1:], None]
            s1 += 1
        elif l.startswith('+'):
            if s2 in line2diffmap:
                line2diffmap[s2][2] = l[1:]
            else:
                line2diffmap[s2] = [s2, None, l[1:]]
            s2 += 1
        else:
            #print 'JUST NORMAL LINE FOR BOTH FILE'
            pass

    return line2diffmap

def getResult(line2diffmap):
    return [line2diffmap[k] for k in sorted(line2diffmap.keys())]

def parse(difflines):
    dm = getDiffMap(difflines)
    return json.dumps(getResult(dm))

if __name__ == '__main__':
    import sys, os
    try:
        difffilepath = sys.argv[1]
    except Exception  as e:
        print "Usage:",sys.argv[0], 'difffile'
        sys.exit(-1)

    # ok
    difflines = open(difffilepath, 'U').readlines()
    diffjson = parse(difflines)
    open('d.json','w').write(diffjson)
    os.system('open d.json')
