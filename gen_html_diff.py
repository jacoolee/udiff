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

print """
<style>
table {-webkit-border-horizontal-spacing: 0; -webkit-border-vertical-spacing: 0;}
td {border-bottom: solid 1px gray; padding-left: 5px; }
.type-mark {display: none; }
.modify {color: purple; }
.delete {color: red; }
.same {}
.add {color: green; }
</style>
"""
print '<table>'

new_used_map = {}
new_ln_map = {i[2]:i[3] for i in op_seqs}

n = 0
total = len(op_seqs)
while n < total:

    op = op_seqs[n]
    typ, ln_old, ln_new, l = op

    if typ == 'L':

        if ln_old is not None:
            ln_old_last = ln_old

        if ln_old:
            if ln_new is None:
                print '<tr class="delete"><td class="type-mark">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%('-', ln_old or '', l, ln_new or '', '')
            else:
                print '<tr class="same"><td class="type-mark">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%('=', ln_old or '', l, ln_new or '', l)
        else:
            if ln_new:
                print '<tr class="add"><td class="type-mark">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%('+', ln_old or '', '', ln_new or '', l)

    elif typ == 'M':
        # print 'dia', ln_old_last, ln_old

        for i in xrange(int(ln_old_last+1), int(ln_old)):
            l = l_map[i]
            print '<tr class="same"><td class="type-mark">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%('F', ln_old or '', l, ln_new or '', l)

    n += 1

print '</table>'
