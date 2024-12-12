#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json

def usage():
    print __file__, "old_file diff_meta_file [--html] [--txt]"
    sys.exit(-1)

if len(sys.argv) < 2:
    usage()

old_file = None
diff_meta_file = None
option_render_txt = False
option_render_html = False

for i in sys.argv[1:]:
    if i.startswith('-'):
        if i == '--html':
            option_render_html = True
        elif i == '--txt':
            option_render_txt = True
        else:
            pass
        continue

    # files
    if old_file is None: # old_file comes first
        old_file = i
    else:
        diff_meta_file = i

if old_file is None or diff_meta_file is None:
    usage()

if not option_render_txt and not option_render_html:
    option_render_txt = True

# https://en.wikipedia.org/wiki/Diff#Unified_format
# https://www.gnu.org/software/diffutils/manual/html_node/Detailed-Unified.html
diff_meta = None
with open(diff_meta_file, "r") as f:
    diff_meta = json.load(f)

ops = diff_meta

f = open(old_file, "r")

l_map = {}
ln = 0
for l in f.readlines():
    ln += 1                     # ln starts from 1

    l = l.replace('\n', '')
    l_map[ln] = l

ln_old_last = 1
ln_new_last = 1

if option_render_html:
    print """
<style>
table {-webkit-border-horizontal-spacing: 0; -webkit-border-vertical-spacing: 0; font-family: monospace; }
td {border-bottom: solid 1px gray; padding-left: 5px; }
.type-mark {display: none; }
.mod {background-color: yellow; color: black; }
.del {background-color: red; color: white;}
.sam {}
.add {background-color: green; color: white;}
</style>
"""
    print '<table>'

def _fli(i=None, max_len=3):
    if i is None:
        return ' '*max_len

    fmt = '%'+str(max_len)+'d'
    return fmt%(i)

# string with fixed length
def _fls(txt=None, max_len=63):
    _txt = txt or ''
    if len(_txt) < max_len:
        return _txt + ' '*(max_len-len(_txt))
    return _txt[0:max_len]

def render(ln_old, s_old, mark, ln_new=None, s_new=None, fli_max_len=3, fls_max_length=63):
    if option_render_txt:
        print \
            _fli(ln_old, max_len=fli_max_len), _fls(s_old, max_len=fls_max_length), \
            mark, \
            _fli(ln_new, max_len=fli_max_len), _fls(s_new, max_len=fls_max_length)

    elif option_render_html:
        if mark == ' ':
            tr_cls = 'sam'
        elif mark == '>':
            tr_cls = 'add'
        elif mark == '<':
            tr_cls = 'del'
        elif mark == '|':
            tr_cls = 'mod'
        else:
            print 'ERROR', 'show never happen'
            tr_cls = ''

        print "<tr class='%s'><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"%(
            tr_cls,
            _fli(ln_old, max_len=fli_max_len), _fls(s_old, max_len=fls_max_length),
            mark,
            _fli(ln_new, max_len=fli_max_len), _fls(s_new, max_len=fls_max_length)
        )

    else:
        pass

idx = 0
total = len(ops)
while idx < total:

    op = ops[idx]
    typ, ln_old, ln_new, l = op

    if typ == 'M':

        # fill up lines missing between hunks
        for i in xrange(int(ln_old_last+1), int(ln_old)):
            l = l_map[i]
            render(ln_old, l, ' ', ln_new, l)

        idx += 1
        continue

    # 'L'

    if ln_old is not None:
        ln_old_last = ln_old
    if ln_new is not None:
        ln_new_last = ln_new

    is_flsame = ln_old and ln_new
    is_minus = not is_flsame and ln_old and not ln_new
    is_plus = not is_flsame and not ln_old and ln_new

    if is_minus:

        if idx+1 == total:      # last one
            render(ln_old, op[3], '<')
            break

        # KEY: probe next op if current is '-' to see if it's '+'
        next_op = ops[idx+1]
        next_typ, next_ln_old, next_ln_new, next_l = next_op

        next_is_flsame = next_ln_old and next_ln_new
        next_is_minus = not next_is_flsame and next_ln_old and not next_ln_new
        next_is_plus = not next_is_flsame and not next_ln_old and next_ln_new

        if next_is_plus:
            render(ln_old, op[3], '|', ln_new or ln_new_last+1, next_op[3])
            idx += 2
            continue
        else:
            render(ln_old, op[3], '<')
            idx += 1
            continue

    if is_plus:
        render(ln_old, '', '>', ln_new, op[3])
        idx += 1
        continue

    if is_flsame:
        render(ln_old, op[3], ' ', ln_new, op[3])
        idx += 1
        continue


if option_render_html:
    print '</table>'
