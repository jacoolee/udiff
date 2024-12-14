#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
import re

if len(sys.argv) < 1:
    print __file__, "diff_file [output_file]"
    sys.exit(-1)

diff_file = sys.argv[1]
output_file = None

if len(sys.argv) > 2:
    output_file = sys.argv[2]

# https://en.wikipedia.org/wiki/Diff#Unified_format
# https://www.gnu.org/software/diffutils/manual/html_node/Detailed-Unified.html

f = open(diff_file, "r")

dm = {}                         # delete map (base on old)
sm = {}                         # delete map (base on old)
am = {}                         # add map (base on new)

ln_old = 0
ln_new = 0

r = []

for l in f.readlines():
    l = l.replace('\n', '')

    if l.startswith('diff '):
        print "      %s"%(l)
        r.append([5, None, None, l, None])
        continue

    if l.startswith('index '):
        print "      %s"%(l)
        r.append([6, None, None, l, None])
        continue

    if l.startswith('---'):
        print "      %s"%(l)
        r.append([3, None, None, l, None])
        continue

    if l.startswith('+++'):
        print "      %s"%(l)
        r.append([4, None, None, l, None])
        continue

    if l.startswith('@@'):
        print "      %s"%(l)

        start, start_count, end, end_count = re.match('@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@', l).groups()
        ln_old = int(start)
        ln_new = int(end)

        start_count = int(start_count)
        end_count = int(end_count)

        # print "ln_old:", ln_old, 'ln_new:', ln_new, 'start_count:', start_count, 'end_count:', end_count
        r.append([2, ln_old, ln_new, start_count, end_count])
        continue

    if l.startswith(' '):
        print "%02d %02d %s"%(ln_old, ln_new, l)
        r.append([0, ln_old, ln_new, l[1:], None])
        ln_old = ln_old + 1
        ln_new = ln_new + 1
        continue

    if l.startswith('-'):
        r.append([-1, ln_old, None, l[1:], None])
        print "%02d    %s"%(ln_old, l)
        ln_old = ln_old + 1
        continue

    if l.startswith('+'):
        r.append([1, None, ln_new, l[1:], None])
        print "   %02d %s"%(ln_new, l)
        ln_new = ln_new + 1
        continue

    # else, ignore

if output_file:
    with open(output_file, 'w') as f:
        f.write(json.dumps(r))

else:
    print json.dumps(r)
