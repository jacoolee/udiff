#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json

if len(sys.argv) < 2:
    print __file__, "old_file diff_meta_file"
    sys.exit(-1)


old_file = sys.argv[1]
diff_meta_file = sys.argv[2]

# https://en.wikipedia.org/wiki/Diff#Unified_format
# https://www.gnu.org/software/diffutils/manual/html_node/Detailed-Unified.html
diff_meta = None
with open(diff_meta_file, "r") as f:
    diff_meta = json.load(f)

op_seqs = diff_meta

f = open(old_file, "r")

l_map = {}
ln = 0
for l in f.readlines():
    ln += 1                     # ln starts from 1

    l = l.replace('\n', '')
    l_map[ln] = l

ln_old_last = 1

for op in op_seqs:
    typ, ln_old, ln_new, l = op

    if typ == 'L':

        if ln_old is not None:
            ln_old_last = ln_old

        if ln_old:
            if ln_new is None:      # delete
                pass
            else:
                # print 'S', l        # same
                print l        # same
        else:
            if ln_new:
                print l        # add

    elif typ == 'M':
        # print 'dia', ln_old_last, ln_old

        for i in xrange(int(ln_old_last+1), int(ln_old)):
            print l_map[i]
