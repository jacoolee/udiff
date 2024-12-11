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

    if l.startswith('---'):
        print "      %s"%(l)
        continue
    if l.startswith('+++'):
        print "      %s"%(l)
        continue
    if l.startswith('@@'):
        print "      %s"%(l)

        start, start_count, end, end_count = re.match('@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@', l).groups()
        ln_old = int(start)
        ln_new = int(end)

        print "ln_old:", ln_old, 'ln_new:', ln_new
        r.append(['M', ln_old, ln_new, None])
        continue

    if l.startswith(' '):
        print "%02d %02d %s"%(ln_old, ln_new, l)
        r.append(['L', ln_old, ln_new, l[1:]])
        ln_old = ln_old + 1
        ln_new = ln_new + 1

    elif l.startswith('-'):
        r.append(['L', ln_old, None, l[1:]])
        print "%02d    %s"%(ln_old, l)
        ln_old = ln_old + 1

    elif l.startswith('+'):
        r.append(['L', None, ln_new, l[1:]])
        print "   %02d %s"%(ln_new, l)
        ln_new = ln_new + 1
    else:
        print 'ERROR: should never happen', ln_old, ln_new
        pass

if output_file:
    with open(output_file, 'w') as f:
        f.write(json.dumps(r))
else:
    print json.dumps(r)
