#! /usr/bin/env python
# -*- coding: utf-8 -*-

# NOTICE: the side-by-side algorithm used here is a simpler one,
# may not compatiable with common-used one that used by other view tools.

from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re
import json

# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Bold
BBlack='\033[1;30m'       # Black
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BYellow='\033[1;33m'      # Yellow
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BCyan='\033[1;36m'        # Cyan
BWhite='\033[1;37m'       # White

# Underline
UBlack='\033[4;30m'       # Black
URed='\033[4;31m'         # Red
UGreen='\033[4;32m'       # Green
UYellow='\033[4;33m'      # Yellow
UBlue='\033[4;34m'        # Blue
UPurple='\033[4;35m'      # Purple
UCyan='\033[4;36m'        # Cyan
UWhite='\033[4;37m'       # White

# Background
On_Black='\033[40m'       # Black
On_Red='\033[41m'         # Red
On_Green='\033[42m'       # Green
On_Yellow='\033[43m'      # Yellow
On_Blue='\033[44m'        # Blue
On_Purple='\033[45m'      # Purple
On_Cyan='\033[46m'        # Cyan
On_White='\033[47m'       # White

# High Intensity
IBlack='\033[0;90m'       # Black
IRed='\033[0;91m'         # Red
IGreen='\033[0;92m'       # Green
IYellow='\033[0;93m'      # Yellow
IBlue='\033[0;94m'        # Blue
IPurple='\033[0;95m'      # Purple
ICyan='\033[0;96m'        # Cyan
IWhite='\033[0;97m'       # White

# Bold High Intensity
BIBlack='\033[1;90m'      # Black
BIRed='\033[1;91m'        # Red
BIGreen='\033[1;92m'      # Green
BIYellow='\033[1;93m'     # Yellow
BIBlue='\033[1;94m'       # Blue
BIPurple='\033[1;95m'     # Purple
BICyan='\033[1;96m'       # Cyan
BIWhite='\033[1;97m'      # White

# High Intensity backgrounds
On_IBlack='\033[0;100m'   # Black
On_IRed='\033[0;101m'     # Red
On_IGreen='\033[0;102m'   # Green
On_IYellow='\033[0;103m'  # Yellow
On_IBlue='\033[0;104m'    # Blue
On_IPurple='\033[0;105m'  # Purple
On_ICyan='\033[0;106m'    # Cyan
On_IWhite='\033[0;107m'   # White

def clear_color():
    # Reset
    global Color_Off
    Color_Off=''       # Text Reset

    # Regular Colors
    global Black        # Black
    global Red          # Red
    global Green        # Green
    global Yellow       # Yellow
    global Blue         # Blue
    global Purple       # Purple
    global Cyan         # Cyan
    global White        # White

    Black=''        # Black
    Red=''          # Red
    Green=''        # Green
    Yellow=''       # Yellow
    Blue=''         # Blue
    Purple=''       # Purple
    Cyan=''         # Cyan
    White=''        # White

    # Bold
    global BBlack       # Black
    global BRed         # Red
    global BGreen       # Green
    global BYellow      # Yellow
    global BBlue        # Blue
    global BPurple      # Purple
    global BCyan        # Cyan
    global BWhite       # White

    BBlack=''       # Black
    BRed=''         # Red
    BGreen=''       # Green
    BYellow=''      # Yellow
    BBlue=''        # Blue
    BPurple=''      # Purple
    BCyan=''        # Cyan
    BWhite=''       # White

    # Underline
    global UBlack       # Black
    global URed         # Red
    global UGreen       # Green
    global UYellow      # Yellow
    global UBlue        # Blue
    global UPurple      # Purple
    global UCyan        # Cyan
    global UWhite       # White

    UBlack=''       # Black
    URed=''         # Red
    UGreen=''       # Green
    UYellow=''      # Yellow
    UBlue=''        # Blue
    UPurple=''      # Purple
    UCyan=''        # Cyan
    UWhite=''       # White

    # Background
    global On_Black       # Black
    global On_Red         # Red
    global On_Green       # Green
    global On_Yellow      # Yellow
    global On_Blue        # Blue
    global On_Purple      # Purple
    global On_Cyan        # Cyan
    global On_White       # White

    On_Black=''       # Black
    On_Red=''         # Red
    On_Green=''       # Green
    On_Yellow=''      # Yellow
    On_Blue=''        # Blue
    On_Purple=''      # Purple
    On_Cyan=''        # Cyan
    On_White=''       # White

    # High Intensity
    global IBlack       # Black
    global IRed         # Red
    global IGreen       # Green
    global IYellow      # Yellow
    global IBlue        # Blue
    global IPurple      # Purple
    global ICyan        # Cyan
    global IWhite       # White

    IBlack=''       # Black
    IRed=''         # Red
    IGreen=''       # Green
    IYellow=''      # Yellow
    IBlue=''        # Blue
    IPurple=''      # Purple
    ICyan=''        # Cyan
    IWhite=''       # White

    # Bold High Intensity
    global BIBlack      # Black
    global BIRed        # Red
    global BIGreen      # Green
    global BIYellow     # Yellow
    global BIBlue       # Blue
    global BIPurple     # Purple
    global BICyan       # Cyan
    global BIWhite      # White

    BIBlack=''      # Black
    BIRed=''        # Red
    BIGreen=''      # Green
    BIYellow=''     # Yellow
    BIBlue=''       # Blue
    BIPurple=''     # Purple
    BICyan=''       # Cyan
    BIWhite=''      # White

    # High Intensity backgrounds
    global On_IBlack   # Black
    global On_IRed     # Red
    global On_IGreen   # Green
    global On_IYellow  # Yellow
    global On_IBlue    # Blue
    global On_IPurple  # Purple
    global On_ICyan    # Cyan
    global On_IWhite   # White

    On_IBlack=''   # Black
    On_IRed=''     # Red
    On_IGreen=''   # Green
    On_IYellow=''  # Yellow
    On_IBlue=''    # Blue
    On_IPurple=''  # Purple
    On_ICyan=''    # Cyan
    On_IWhite=''   # White


def usage():
    print __file__, "[diff_json_file|-] [-h|--help] [--all|-a old_file] [--html|-l] [--txt|-t] [--json|-j] [--color|-c] [--no-color|-C] [--width|-w width] [--bychar|-r]"
    print '    diff_json_file     : reads from `diff_json_file` or stdin if `-` given'
    print '    -h | --help        : help'
    print '    -a | --all         : old_file print whole content with diff and same content compared to the old_file'
    print '    -l | --html        : print diff in html'
    print '    -t | --txt         : print diff in plain txt, enabled by default'
    print '    -j | --json        : print diff in json'
    print '    -c | --color       : show color, usable with `--txt`'
    print '    -C | --no-color    : disable color, usable with `--txt`'
    print '    -w | --width width : set char counts to be show for a diff line'
    print '    -r | --bychar      : diff old line with new line with comparing char by char, default is LCS algorithm'

def _fli(i=None, char=' ', max_len=5):
    if i is None:
        return char*max_len

    fmt = '%'+str(max_len)+'d'
    return fmt%(i)

# string with fixed length
def _fls(txt=None):
    global option_width
    max_len = option_width
    _txt = txt or ''

    if len(_txt) < max_len:
        return _txt + ' '*(max_len-len(_txt))
    return _txt[0:max_len]

def html_escape(code_text):
    # https://stackoverflow.com/questions/7381974/which-characters-need-to-be-escaped-in-html#7382028
    return code_text\
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

def render_header(l):
    if option_render_txt:
        print l
    elif option_render_html:
        print '<tr><td/><td>',html_escape(l),'</td><td/><td/><td/></tr>'
    else:
        pass

g_is_first_diff_header_printed = False
def render_diff_header(l):
    global g_is_first_diff_header_printed
    if g_is_first_diff_header_printed:
        if option_render_txt:
            print "%s%s%s%s"%('\n', On_Green, l, Color_Off)
        elif option_render_html:
            print '<tr><td> </td><td/><td/><td/><td/></tr>'
            print '<tr class="diff_header"><td/><td>%s</td><td/><td/><td/></tr>'%(html_escape(_fls(l)))
        else:
            pass
    else:
        if option_render_txt:
            print "%s%s%s"%(On_Green, l, Color_Off)
        elif option_render_html:
            print '<tr class="diff_header"><td/><td>%s</td><td/><td/><td/></tr>'%(html_escape(_fls(l)))
        else:
            pass

        g_is_first_diff_header_printed = True

def render_file_header(l):
    if option_render_txt:
        if l.startswith('---'):
            print l
        else:
            print l
    elif option_render_html:
        if l.startswith('---'):
            print '<tr><td/><td>',html_escape(_fls(l)),'</td><td/><td/><td/></tr>'
        else:
            print '<tr><td/><td>',html_escape(_fls(l)),'</td><td/><td/><td/></tr>'

def render_hunk_separator(op):
    _, ln_old, ln_new, start_count, end_count = op
    if option_render_txt:
        c = Blue

        # use same format as render_line to keep length same
        print '%s%s%s%s_%s%s%s%s%s%s%s%s%s%s'%(
            '',
            c,
            c,
            _fli(None, '_'),
            Color_Off,
            c,
            _fls('_'*1000),
            '_',       # do no show tailing spaces
            c,
            _fli(None, '_'),
            Color_Off,
            c,
            '_'+_fls('_'*1000),
            Color_Off
        )

        print '@@ -%d,%s +%d,%s @@%s'%(ln_old, start_count or '', ln_new, end_count or '', Color_Off)

    elif option_render_html:
        l = '@@ -%d,%s +%d,%s @@'%(ln_old, start_count or '', ln_new, end_count or '')
        print "<tr class='hunk_head'><td/><td>%s</td><td/><td/><td/></tr>"%(html_escape(_fls(l)))

    else:
        pass

def line_diff_by_LCS(ol, nl, mark, c):

    def tokenize_line(line):
        """Splits a line into words and punctuation tokens to keep formatting intact."""

        # This regex captures words (\w+) or any non-whitespace sequence (\S)
        return re.findall(r'\w+|\s+|[^\w\s]', line)

    def compute_lcs_matrix(old_tokens, new_tokens):
        """Builds a classic Dynamic Programming table to **find the Longest Common Subsequence.**"""

        m, n = len(old_tokens), len(new_tokens)
        # Create an (m+1) x (n+1) matrix initialized to 0
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if old_tokens[i - 1] == new_tokens[j - 1]:
                    same='=='
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    same='!='
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp

    def _f(code_text):
        return html_escape(code_text) if option_render_html else code_text

    ################################################################
    """main start"""
    """Executes Pass 2: Tokenizes lines and backtracks through the LCS matrix."""

    line_modified = mark == MARK_MOD

    del_marker_prefix = Black+''+On_Red if line_modified else c
    del_marker_postfix = c

    add_marker_prefix = Black+''+On_Green if line_modified else c
    add_marker_postfix = c

    if option_render_html:
        del_marker_prefix = '<span class="char_old">'
        del_marker_postfix = '</span>'

        add_marker_prefix = '<span class="char_new">'
        add_marker_postfix = '</span>'

    ################################################################

    old_tokens = tokenize_line(ol)
    new_tokens = tokenize_line(nl)

    dp = compute_lcs_matrix(old_tokens, new_tokens)

    # Backtrack from the bottom-right of the matrix to build the diff
    i, j = len(old_tokens), len(new_tokens)
    rst_old = []
    rst_new = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and old_tokens[i - 1] == new_tokens[j - 1]:
            # Token is identical in both lines
            rst_old.append(old_tokens[i - 1])
            rst_new.append(new_tokens[j - 1])

            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            # Token was inserted in the new line
            # rst_new.append(f"{{+{new_tokens[j - 1]}+}}")
            v = "%s%s%s"%(add_marker_prefix, _f(new_tokens[j - 1]), add_marker_postfix)
            rst_new.append(v)
            j -= 1
        else:
            # Token was deleted from the old line
            v = "%s%s%s"%(del_marker_prefix, _f(old_tokens[i - 1]), del_marker_postfix)
            rst_old.append(v)
            i -= 1

    # Since we backtracked from the end, reverse the list to get the correct order
    _ol = "".join(reversed(rst_old))
    _nl = "".join(reversed(rst_new))

    if option_render_txt:
        ol_tailing_spaces = ' '*(option_width - len(ol))
        _ol += ol_tailing_spaces

    return _ol, _nl

def line_diff_by_char(ol, lenol, nl, lennl, c=''):
    _ol = ''
    _nl = ''
    pretext_same=True
    li=0
    i=0

    length = min(lenol, lennl)

    while i<length:
        if ol[i] == nl[i]:
            if pretext_same:
                i += 1
                pretext_same=True
            else:               # unsame to same (idx:i)
                if option_render_html:
                    _ol += html_escape(ol[li:i])+'</span>'
                    _nl += html_escape(nl[li:i])+'</span>'
                else:
                    _ol += ol[li:i]+c
                    _nl += nl[li:i]+c

                li=i

                i += 1
                pretext_same=True
        else:
            if pretext_same:    # same to unsame (idx:i)
                if option_render_html:
                    _ol += html_escape(ol[li:i])+'<span class="char_old">'
                    _nl += html_escape(nl[li:i])+'<span class="char_new">'
                else:
                    _ol += ol[li:i]+Black+''+On_Red
                    _nl += nl[li:i]+Black+''+On_Green

                li=i

                i += 1
                pretext_same=False
            else:
                i += 1
                pretext_same=False

    if li != i:
        if option_render_html:
            _ol += html_escape(ol[li:i])+'</span>'
            _nl += html_escape(nl[li:i])+'</span>'
        else:
            _ol += ol[li:i]+c
            _nl += nl[li:i]+c

    if option_render_html:
        _ol += html_escape(ol[i:])
        _nl += html_escape(nl[i:])
    else:
        ol_tailing_spaces = ' '*(option_width - len(ol))
        _ol += ol[i:] + ol_tailing_spaces
        _nl += nl[i:]

    return _ol, _nl

def render_line(ln_old, s_old, mark, ln_new=None, s_new=None):
    if option_render_json:
        global json_list
        json_list.append([mark, ln_old, s_old, ln_new, s_new])

    elif option_render_txt:

        if mark == MARK_SAME:
            c = ''
        elif mark == MARK_ADD:
            c = Green
        elif mark == MARK_DEL:
            c = Red
        elif mark == MARK_MOD:
            c = Yellow
        else:
            c = ''

        s_old = s_old or ''
        s_new = s_new or ''

        # at lest '1' loop turn to ensure empty line get chance to show
        t = max(len(s_old), len(s_new), 1)
        i = 0

        while i < t:
            i_ = i+option_width

            # TODO [2026-09-20 17:57:01]: apply color to s_old and s_new diff parts
            _o = s_old[i:i_]
            _n = s_new[i:i_]

            ol, nl = line_diff_by_LCS(_o, _n, mark, c) if option_by_lcs else line_diff_by_char(_fls(_o), len(_o), _n, len(_n), c)

            print '%s%s%s%s %s%s%s%s%s%s%s%s%s%s'%(
                '' if option_color else mark+' ',
                c,
                c,
                _fli(ln_old if i==0 else None),
                Color_Off,
                c,
                ol,
                '\u200B',       # do no show tailing spaces
                c,
                _fli(ln_new if i==0 else None) if ln_new else '',
                Color_Off,
                c,
                ' '+nl if nl else nl,
                Color_Off
            )
            i = i_

    elif option_render_html:
        if mark == MARK_SAME:
            tr_cls = 'sam'
        elif mark == MARK_ADD:
            tr_cls = 'add'
        elif mark == MARK_DEL:
            tr_cls = 'del'
        elif mark == MARK_MOD:
            tr_cls = 'mod'
        else:
            tr_cls = ''

        s_old = s_old or ''
        s_new = s_new or ''

        t = max(len(s_old), len(s_new), 1)
        i = 0

        while i < t:
            i_ = i+option_width

            _o = s_old[i:i_]
            _n = s_new[i:i_]

            ol, nl = line_diff_by_LCS(_o, _n, mark, '') if option_by_cls else line_diff_by_char(_fls(_o), len(_o), _n, len(_n))

            print "<tr class='%s'><td class='ln_old'>%s</td><td>%s</td><td>%s</td><td class='ln_new'>%s</td><td>%s</td></tr>"%(
                tr_cls,
                _fli(ln_old if i==0 else None),
                html_escape(ol) if mark == MARK_SAME else ol,
                '', # mark,
                _fli(ln_new if i==0 else None),
                html_escape(nl) if mark == MARK_SAME else nl
            )
            i = i_

    else:
        pass

################################################################
# main

if len(sys.argv) < 2:
    usage()
    sys.exit(-1)

old_file = None
diff_json_file = None

option_render_txt = False
option_render_json = False
option_render_html = False
option_color = False
option_width = 70
option_by_lcs = True

idx = 1                         # start from first parameter
while idx < len(sys.argv):
    i = sys.argv[idx]
    if i.startswith('-'):
        if i == '--help' or i == '-h':
            usage()
            sys.exit(0)

        if i == '-':            # use stdin as input
            pass
        elif i == '--html' or i == '-l':
            option_render_html = True
        elif i == '--txt' or i == '-t':
            option_render_txt = True
        elif i == '--bychar' or i == '-r':
            option_by_lcs = False
        elif i == '--json' or i == '-j':
            option_render_json = True
        elif i == '--color' or i == '-c':
            option_color = True
        elif i == '--no-color' or i == '-C':
            option_color = False
            clear_color()
        elif i == '--all' or i == '-a':
            try:
                old_file = sys.argv[idx+1]
            except Exception as e:
                usage()
                print i, 'expects an old_file as its argument'
                sys.exit(-1)

            idx += 1
        elif i == '--width' or i == '-w':
            try:
                option_width = int(sys.argv[idx+1])
            except Exception as e:
                usage()
                print i, 'expects an number as its argument'
                sys.exit(-1)

            idx += 1
        else:
            print 'Error: unknown parameter:', i
            sys.exit(-1)

        idx += 1

    else:
        diff_json_file = i

        idx += 1

if not option_render_txt and not option_render_html:
    option_render_txt = True

# https://en.wikipedia.org/wiki/Diff#Unified_format
# https://www.gnu.org/software/diffutils/manual/html_node/Detailed-Unified.html
diff_meta = None

if diff_json_file:
    with open(diff_json_file, "r") as f:
        diff_meta = json.load(f)
else:
    diff_meta = json.load(sys.stdin)

ops = diff_meta

if old_file:
    f = open(old_file, "r")

    l_map = {}
    ln = 0
    for l in f.readlines():
        ln += 1                     # ln starts from 1
        l = l.replace('\n', '')
        l_map[ln] = l

    ln_old_total = ln

    f.close()

ln_old_last = 0
ln_new_last = 0

if option_render_html:
    print """
<style>
.theme-dark {background-color: #111; color: #ddd; }
table {border-collapse: collapse; -webkit-border-horizontal-spacing: 0; -webkit-border-vertical-spacing: 0; font-family: monospace; cursor: default; }
td {white-space: pre; padding-left: 5px;}
.diff_header { background-color: green; color: white;}
tr.hunk_head > td { border-top: solid 1px blue; }
.ln_old,.ln_new {color: gray};
.type-mark {display: none; }
.mod, .mod .ln_old, .mod .ln_new {color: goldenrod; }
.del, .del .ln_old {color: red;}
.sam {}
.add, .add .ln_new {color: green;}
.char_old {background-color: red; color: black;}
.char_new {background-color: lightgreen; color: black;}
</style>
"""

if option_render_html:
    print """
<html>
  <script>
     document.addEventListener('DOMContentLoaded', () => {
     const dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
     document.documentElement.classList.toggle('theme-dark', dark);
});
  </script>
<table>
"""

idx = 0
total = len(ops)

if old_file:
    if total == 0:
        for i in xrange(1, ln_old_total+1):
            l = l_map[i]
            render_line(i, l, MARK_SAME, i, l)

        if option_render_html:
            print '</table></html>'

while idx < total:
    op = ops[idx]
    typ, ln_old, ln_new, l, _ = op

    if typ == 2:                # hunk meta line
        if old_file:
            # fill up lines missing between hunks
            n = 0
            for i in xrange(int(ln_old_last+1), int(ln_old)):
                n += 1
                l = l_map[i]
                render_line(ln_old_last+n, l, MARK_SAME, ln_new_last + n, l)

        else:
            render_hunk_separator(op)

        idx += 1
        continue

    if typ == 3 or typ == 4:
        render_file_header(l)
        idx += 1
        continue

    if typ == 5:
        render_diff_header(l)
        idx += 1
        continue

    if typ == 6:
        render_header(l)
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

        # idx2 exceeds ops or 3,4,5,6 matched, which means, all from idx to idx2 (exclusive) are '-'
        if idx2 == total or ops[idx2][0] > 2:
            for _op in ops[idx: idx2]:
                _typ, _lno, _lnn, _l, _ = _op

                if _lno: ln_old_last = _lno
                if _lnn: ln_new_last = _lnn

                render_line(_lno, _l, MARK_DEL)

            idx = idx2
            continue

        if ops[idx2][0] == 0:   # idx2 points to first ' ' after bunch of '-'
            for _op in ops[idx: idx2]:
                _typ, _lno, _lnn, _l, _ = _op

                if _lno: ln_old_last = _lno
                if _lnn: ln_new_last = _lnn

                render_line(_lno, _l, MARK_DEL)

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
                    _, _lno_l, _lnn_l, _l_l, _ = ops[idx+_i]
                    _, _lno_r, _lnn_r, _l_r, _ = ops[idx2+_i]

                    if _lno_l: ln_old_last = _lno_l
                    if _lnn_r: ln_new_last = _lnn_r

                    render_line(_lno_l, _l_l, MARK_MOD, _lnn_r, _l_r)

                for _op in ops[idx2+n_minus:idx3]: # idx3 not cosumned
                    _typ, _lno, _lnn, _l, _ = _op

                    if _lno: ln_old_last = _lno
                    if _lnn: ln_new_last = _lnn

                    render_line(None, None, MARK_ADD, _lnn, _l)

                # go on to next round
                idx = idx3
                continue

            else:               # n_minus > n_plus
                for _op in ops[idx:idx+n_minus-n_plus]:
                    _typ, _lno, _lnn, _l, _ = _op

                    if _lno: ln_old_last = _lno
                    if _lnn: ln_new_last = _lnn

                    render_line(_lno, _l, MARK_DEL)

                # cosume both n_plus count of '-' ops and n_minus count of '+' ops
                _idx = idx+n_minus-n_plus
                for _i in xrange(0, n_plus):
                    _, _lno_l, _lnn_l, _l_l, _ = ops[_idx+_i]
                    _, _lno_r, _lnn_r, _l_r, _ = ops[idx2+_i]

                    if _lno_l: ln_old_last = _lno_l
                    if _lnn_r: ln_new_last = _lnn_r

                    render_line(_lno_l, _l_l, MARK_MOD, _lnn_r, _l_r)


                # go on to next round
                idx = idx3
                continue

    if typ == 1:                # plus '+'
        render_line(ln_old, None, MARK_ADD, ln_new, l)
        idx += 1
        continue

    if typ == 0:                # space/same ' '
        render_line(ln_old, l, MARK_SAME, ln_new, l)
        idx += 1
        continue

# padding last parts (not included in hunk) if exists from old file
if old_file and ln_old_last > 0:             # means have been re-assigned by 'L' type meta
    n = 0
    for i in xrange(ln_old_last+1, ln_old_total+1):
        n += 1
        l = l_map[i]
        render_line(i, l, MARK_SAME, ln_new_last+n, l)

if option_render_html:
    print '</table>'

if option_render_json:
    print json.dumps(json_list)
