#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json

def usage():
    print __file__, "old_file diff_json_file [--html] [--txt] [--json]"
    sys.exit(-1)

def _fli(i=None, max_len=5):
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

def html_escape(txt):
    # https://stackoverflow.com/questions/7381974/which-characters-need-to-be-escaped-in-html#7382028
    return txt\
        .replace('&', '&amp')\
        .replace('>', '&gt')\
        .replace('<', '&lt')\
        .replace('"', '&quot')\
        .replace("'", '&#39')

json_list = []

MARK_SAME = ' '
MARK_ADD = '+'
MARK_DEL = '-'
MARK_MOD = '|'
MARK_NONE = ''

def render(ln_old, s_old, mark, ln_new=None, s_new=None):
    if option_render_json:
        global json_list
        json_list.append([mark, ln_old, s_old, ln_new, s_new])

    elif option_render_txt:
        print \
            _fli(ln_old), _fls(s_old), \
            mark, \
            _fli(ln_new), _fls(s_new)

    elif option_render_html:
        if mark == ' ':
            tr_cls = 'sam'
        elif mark == MARK_ADD:
            tr_cls = 'add'
        elif mark == MARK_DEL:
            tr_cls = 'del'
        elif mark == MARK_MOD:
            tr_cls = 'mod'
        else:
            tr_cls = ''

        print "<tr class='%s'><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"%(
            tr_cls,
            _fli(ln_old, max_len=fli_max_len),
            html_escape(_fls(s_old, max_len=fls_max_length)),
            mark,
            _fli(ln_new, max_len=fli_max_len),
            html_escape(_fls(s_new, max_len=fls_max_length))
        )

    else:
        pass

################################################################
# main

if len(sys.argv) < 2:
    usage()

old_file = None
diff_json_file = None
option_render_txt = False
option_render_json = False
option_render_html = False

for i in sys.argv[1:]:
    if i.startswith('-'):
        if i == '--html':
            option_render_html = True
        elif i == '--txt':
            option_render_txt = True
        elif i == '--json':
            option_render_json = True
        else:
            pass
        continue

    # files
    if old_file is None: # old_file comes first
        old_file = i
    else:
        diff_json_file = i

if old_file is None or diff_json_file is None:
    usage()

if not option_render_txt and not option_render_html:
    option_render_txt = True

# https://en.wikipedia.org/wiki/Diff#Unified_format
# https://www.gnu.org/software/diffutils/manual/html_node/Detailed-Unified.html
diff_meta = None
with open(diff_json_file, "r") as f:
    diff_meta = json.load(f)

ops = diff_meta

f = open(old_file, "r")

l_map = {}
ln = 0
for l in f.readlines():
    ln += 1                     # ln starts from 1

    l = l.replace('\n', '')
    l_map[ln] = l
ln_old_total = ln

ln_old_last = 0
ln_new_last = 0

if option_render_html:
    print """
<style>
table {-webkit-border-horizontal-spacing: 0; -webkit-border-vertical-spacing: 0; font-family: monospace; }
td {white-space: pre; border-bottom: solid 1px gray; padding-left: 5px; }
.type-mark {display: none; }
.mod {background-color: yellow; color: black; }
.del {background-color: red; color: white;}
.sam {}
.add {background-color: green; color: white;}
</style>
"""

if option_render_html:
    print '<table>'

    for op in ops:
        typ, ln_old, ln_new, l = op
        if typ == 2:
            print '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%('meta: ln_old:', str(ln_old), 'ln_new:', str(ln_new))
        elif typ == -1:
            print '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(ln_old, '', MARK_DEL, html_escape(l))
        elif typ == 0:
            print '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(ln_old, ln_new, ' ', html_escape(l))
        elif typ == 1:
            print '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%('', ln_new, MARK_ADD, html_escape(l))
        else:
            pass

    print '</table>'
    print '<br/>'

if option_render_html:
    print '<table>'

idx = 0
total = len(ops)

if total == 0:
    for i in xrange(1, ln_old_total+1):
        l = l_map[i]
        render(i, l, MARK_SAME, i, l)

    if option_render_html:
        print '</table>'

while idx < total:
    op = ops[idx]
    typ, ln_old, ln_new, l = op

    if typ == 2:                # hunk meta line
        # fill up lines missing between hunks
        n = 0
        for i in xrange(int(ln_old_last+1), int(ln_old)):
            n += 1
            l = l_map[i]
            render(ln_old_last+n, l, MARK_SAME, ln_new_last + n, l)

        idx += 1
        continue

    # else, data lines
    if ln_old is not None:
        ln_old_last = ln_old
    if ln_new is not None:
        ln_new_last = ln_new

    if typ == -1:               # minus '-'
        # consume consequent '-' as much as possible
        idx2 = idx + 1
        while idx2 < total and ops[idx2][0] == -1:
            idx2 += 1

        if idx2 == total:       # idx2 exceeds ops, which means, all from idx is '-'
            for _op in ops[idx: idx2]:
                _typ, _lno, _lnn, _l = _op

                if _lno: ln_old_last = _lno
                if _lnn: ln_new_last = _lnn

                render(_lno, _l, MARK_DEL)

            # print 'dia: idx2 = %d, total = %d'%(idx2, total)
            break               # all done, just break main loop

        if ops[idx2][0] == 0:   # idx2 points to first ' ' after bunch of '-'
            for _op in ops[idx: idx2]:
                _typ, _lno, _lnn, _l = _op

                if _lno: ln_old_last = _lno
                if _lnn: ln_new_last = _lnn

                render(_lno, _l, MARK_DEL)

            # go on to next round
            idx = idx2
            continue

        if ops[idx2][0] == 1:   # idx2 points to first '+' after bunch of '-'
            # consume consequent '+' as much as possible
            idx3 = idx2 + 1
            while idx3 < total and ops[idx3][0] == 1:
                idx3 += 1

            # either idx3 is last op, or points to ' ', '-',
            # we all terminate this round

            n_minus = idx2 - idx
            n_plus = idx3 - idx2

            if n_minus <= n_plus:
                # cosume both n_minus count of '-' ops and n_minus count of '+' ops
                for _i in xrange(0, n_minus):
                    _, _lno_l, _lnn_l, _l_l = ops[idx+_i]
                    _, _lno_r, _lnn_r, _l_r = ops[idx2+_i]

                    if _lno_l: ln_old_last = _lno_l
                    if _lnn_r: ln_new_last = _lnn_r

                    render(_lno_l, _l_l, MARK_MOD, _lnn_r, _l_r)

                for _op in ops[idx2+n_minus:idx3]: # idx3 not cosumned
                    _typ, _lno, _lnn, _l = _op

                    if _lno: ln_old_last = _lno
                    if _lnn: ln_new_last = _lnn

                    render(None, None, MARK_ADD, _lnn, _l)

                # go on to next round
                idx = idx3
                continue

            else:               # n_minus > n_plus
                for _op in ops[idx:idx+n_minus-n_plus]:
                    _typ, _lno, _lnn, _l = _op

                    if _lno: ln_old_last = _lno
                    if _lnn: ln_new_last = _lnn

                    render(_lno, _l, MARK_DEL)

                # cosume both n_plus count of '-' ops and n_minus count of '+' ops
                _idx = idx+n_minus-n_plus
                for _i in xrange(0, n_plus):
                    _, _lno_l, _lnn_l, _l_l = ops[_idx+_i]
                    _, _lno_r, _lnn_r, _l_r = ops[idx2+_i]

                    if _lno_l: ln_old_last = _lno_l
                    if _lnn_r: ln_new_last = _lnn_r

                    render(_lno_l, _l_l, MARK_MOD, _lnn_r, _l_r)


                # go on to next round
                idx = idx3
                continue

    if typ == 1:                # plus '+'
        render(ln_old, None, MARK_ADD, ln_new, l)
        idx += 1
        continue

    if typ == 0:                # space/same ' '
        render(ln_old, l, MARK_SAME, ln_new, l)
        idx += 1
        continue

# padding last parts (not included in hunk) if exists from old file
if ln_old_last > 0:             # means have been re-assigned by 'L' type meta
    n = 0
    for i in xrange(ln_old_last+1, ln_old_total+1):
        n += 1
        l = l_map[i]
        render(i, l, MARK_SAME, ln_new_last+n, l)

if option_render_html:
    print '</table>'

if option_render_json:
    print json.dumps(json_list)
