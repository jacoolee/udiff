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

def usage():
    print __file__, "[diff_json_file|-] [-h|--help] [--all|-a old_file] [--html|-l] [--txt|-t] [--json|-j] [--color|-c] [--no-color|-C] [--width|-w width]"
    print '    diff_json_file     : reads from `diff_json_file` or stdin if `-` given'
    print '    -h | --help        : help'
    print '    -a | --all         : old_file print whole content with diff and same content compared to the old_file'
    print '    -l | --html        : print diff in html'
    print '    -t | --txt         : print diff in plain txt, enabled by default'
    print '    -j | --json        : print diff in json'
    print '    -c | --color       : show color, usable with `--txt`'
    print '    -C | --no-color    : disable color, usable with `--txt`'
    print '    -w | --width width : set char counts to be show for a diff line'

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
        print '<div>%s</div>'%(html_escape(l))
    else:
        pass

def render_diff_header(l, is_first_diff_header):
    """diff --git a/file b/file"""
    if option_render_txt:
        print "%s%s%s%s"%('\n' if not is_first_diff_header else '', On_Purple if option_color else '', l, Color_Off if option_color else '')
    elif option_render_html:
        if not is_first_diff_header:
            print "</table><br/>"
        print '<div class="diff_header">%s</div>'%(html_escape(l))
    else:
        pass

def render_file_header(l):
    if option_render_txt:
        print l
    elif option_render_html:
        print '<div>%s</div>'%(html_escape(l))

def render_hunk_separator(op, filename, is_first_hunk):
    _, ln_old, ln_new, start_count, end_count = op
    if option_render_txt:
        c = Blue if option_color else ''
        c_off = Color_Off if option_color else ''

        # use same format as render_line to keep length same
        print '%s%s%s%s_%s%s%s%s%s%s%s%s%s%s'%(
            '',
            c,
            c,
            _fli(None, '_'),
            c_off,
            c,
            _fls('_'*1000),
            '_',       # do no show tailing spaces
            c,
            _fli(None, '_'),
            c_off,
            c,
            '_'+_fls('_'*1000),
            c_off
        )

        print '@@ -%d,%s +%d,%s @@ %s%s'%(ln_old, start_count or '', ln_new, end_count or '', filename, c_off)

    elif option_render_html:
        l = '@@ -%d,%s +%d,%s @@ %s'%(ln_old, start_count or '', ln_new, end_count or '', filename)
        if not is_first_hunk:
            print "</table>"
        print "<div class='hunk_head'>%s</div>"%(html_escape(l))
        print "<table>"

    else:
        pass

def parse_line_diff_by_LCS(ol, nl):

    def tokenize_line(line):
        """Splits a line into words and punctuation tokens to keep formatting intact."""

        # by Google AI
        # stanard: This regex captures words (\w+) or any non-whitespace sequence (\S)

        regex_standard = r'\w+|\s+|[^\w\s]'
        regex_char_level = r'.' # ultra-precise
        regex_advanced = r'(\d+(?:\.\d+)?|==|!=|<=|>=|&&|\|\||\+\+|--|\w+|\s+|[^\w\s])'

        return re.findall(regex_standard, line)

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

    ################################################################
    """main start"""
    """Executes Pass 2: Tokenizes lines and backtracks through the LCS matrix."""

    old_tokens = tokenize_line(ol)
    new_tokens = tokenize_line(nl)

    dp = compute_lcs_matrix(old_tokens, new_tokens)

    # Backtrack from the bottom-right of the matrix to build the diff
    i, j = len(old_tokens), len(new_tokens)
    meta_old = []
    meta_new = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and old_tokens[i - 1] == new_tokens[j - 1]:
            # Token is identical in both lines
            v = [0,old_tokens[i - 1]]
            meta_old.append(v)
            meta_new.append(v)

            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            # Token was inserted in the new line
            v = [1,new_tokens[j - 1]]
            meta_new.append(v)
            j -= 1
        else:
            # Token was deleted from the old line
            v = [-1,old_tokens[i - 1]]
            meta_old.append(v)
            i -= 1

    # Since we backtracked from the end, reverse the list to get the correct order
    return list(reversed(meta_old)), list(reversed(meta_new))

def render_line_diff_by_LCS(ln_old, ln_new, s_old, s_new, mark):
    c = ''
    c_off = Color_Off if option_color else ''

    line_modified = mark == MARK_MOD

    del_marker_prefix = (White+''+On_Red if option_color else '') if line_modified else c
    del_marker_postfix = c
    add_marker_prefix = (White+''+On_Green if option_color else '') if line_modified else c
    add_marker_postfix = c

    if option_color:
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

    ################################################################

    meta_ol, meta_nl = parse_line_diff_by_LCS(s_old, s_new)

    i = 0
    # t should be at lest '1' loop turn to ensure empty line get chance to show
    t = max(len(s_old), len(s_new), 1)

    meta_ol_item_exceed = None
    meta_nl_item_exceed = None

    meta_ol_idx = 0
    meta_nl_idx = 0

    l1 = None                   # list of item for render part of old_line within option_width
    l2 = None                   # list of item for render part of new_line within option_width

    while i < t:
        i_ = i+option_width

        l1 = [meta_ol_item_exceed] if meta_ol_item_exceed else []
        l2 = [meta_nl_item_exceed] if meta_nl_item_exceed else []

        # clear after used
        meta_ol_item_exceed = None
        meta_nl_item_exceed = None

        # compose l1
        len_ol = i
        len_meta_ol = len(meta_ol)
        while meta_ol_idx < len_meta_ol:
            item = meta_ol[meta_ol_idx]
            item_type, item_token = item
            len_token = len(item_token)
            len_ol += len_token
            if len_ol < i_:
                l1.append(item)
                meta_ol_idx += 1
                continue
            elif len_ol == i_:   # exactly found
                l1.append(item)
                meta_ol_idx += 1
                break
            else:               # found, but len_ol exceeds i_
                # split the item
                len_exceed = len_ol - i_
                idx_ = len_token - len_exceed
                vl = [item_type, item_token[0:idx_]]
                meta_ol_item_exceed = [item_type, item_token[idx_:]] # exceed part
                l1.append(vl)
                meta_ol_idx += 1
                break

        # compose l2
        len_nl = i
        len_meta_nl = len(meta_nl)
        while meta_nl_idx < len_meta_nl:
            item = meta_nl[meta_nl_idx]
            item_type, item_token = item
            len_token = len(item_token)
            len_nl += len_token
            if len_nl < i_:
                l2.append(item)
                meta_nl_idx += 1
                continue
            elif len_nl == i_:   # exactly found
                l2.append(item)
                meta_nl_idx += 1
                break
            else:               # found, but len_nl exceeds i_
                # split the item
                len_exceed = len_nl - i_
                idx_ = len_token - len_exceed
                vl = [item_type, item_token[0:idx_]]
                meta_nl_item_exceed = [item_type, item_token[idx_:]] # exceed part
                l2.append(vl)
                meta_nl_idx += 1
                break


        # compose ol by l1
        ol = ''
        len_raw_ol = 0
        for item in l1:
            item_type, item_token = item
            ol += "%s%s%s"%(
                c if item_type == 0 else del_marker_prefix,
                item_token,
                c if item_type == 0 else del_marker_postfix
            )
            len_raw_ol += len(item_token)

        if len_raw_ol < option_width:
            ol_tailing_spaces = ' '*(option_width - len_raw_ol)
            ol += c_off + ol_tailing_spaces

        # compose nl by l2
        nl = ''
        for item in l2:
            item_type, item_token = item
            nl += "%s%s%s"%(
                c if item_type == 0 else add_marker_prefix,
                item_token,
                c if item_type == 0 else add_marker_postfix
            )

        print '%s%s%s%s %s%s%s%s%s%s%s%s%s%s'%(
            '' if option_color else mark+' ',
            c,
            c,
            _fli(ln_old if i==0 else None),
            c_off,
            c,
            ol ,
            '\u200B',       # do no show tailing spaces
            c,
            _fli(ln_new if i==0 else None) if ln_new else '',
            c_off,
            c,
            ' '+nl if nl else nl,
            c_off
        )

        # next turn
        i = i_

def render_line_diff_by_LCS_html(ln_old, ln_new, s_old, s_new, mark):
    def _f(code_text):
        return html_escape(code_text) if option_render_html else code_text

    tr_cls = ''
    line_modified = mark == MARK_MOD

    del_marker_prefix = '<span class="token token_old">' if line_modified else '<span class="token">'
    del_marker_postfix = '</span>'
    add_marker_prefix = '<span class="token token_new">' if line_modified else '<span class="token">'
    add_marker_postfix = '</span>'

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

    ################################################################

    meta_ol, meta_nl = parse_line_diff_by_LCS(s_old, s_new)

    # TODO: need optimize
    ol = ''
    for t_type,t_text in meta_ol:
        if t_type == 0:
            ol += '<span class="token">%s</span>'%(html_escape(t_text))
        elif t_type == -1:
            ol += '<span class="token token_old">%s</span>'%(html_escape(t_text))
        elif t_type == 1:
            ol += '<span class="token token_new">%s</span>'%(html_escape(t_text))
        else:
            pass

    nl = ''
    for t_type,t_text in meta_nl:
        if t_type == 0:
            nl += '<span class="token">%s</span>'%(html_escape(t_text))
        elif t_type == -1:
            nl += '<span class="token token_old">%s</span>'%(html_escape(t_text))
        elif t_type == 1:
            nl += '<span class="token token_new">%s</span>'%(html_escape(t_text))
        else:
            pass

    print "<tr class='%s'><td valign='top' class='ln_old'>%s</td><td halign='left' class='ol'>%s</td><td valign='top' class='ln_new'>%s</td><td halign='left' class='nl'>%s</td></tr>"%(
        tr_cls,
        _fli(ln_old),
        ol,
        _fli(ln_new),
        nl
    )

def render_line(ln_old, s_old, mark, ln_new=None, s_new=None):
    if option_render_json:
        global json_list
        json_list.append([mark, ln_old, s_old, ln_new, s_new])

    elif option_render_txt:
        render_line_diff_by_LCS(ln_old, ln_new, s_old or '', s_new or '', mark)
    elif option_render_html:
        render_line_diff_by_LCS_html(ln_old, ln_new, s_old or '', s_new or '', mark)
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
        elif i == '--json' or i == '-j':
            option_render_json = True
        elif i == '--color' or i == '-c':
            option_color = True
        elif i == '--no-color' or i == '-C':
            option_color = False
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

aligned_output = diff_meta

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
    print """<!DOCTYPE html>
<html>
  <head>
    <style>
      html { --tr-bg: #ccc; --font-size: 13px; font-family: monospace; font-size: var(--font-size); background-color: #EEEEF0; cursor: default; }
      .theme-dark { --tr-bg: #333; background-color: rgb(17, 17, 17); color: rgb(221, 221, 221); }
      table { width: 100%; border-collapse: collapse; font-size: var(--font-size); }
      tr { width: 100%; }
      .diff_header { background-color: purple; color: white; display: initial; }
      .hunk_head { border-top: 1px solid blue; }
      .ln_old, .ln_new { color: gray; opacity: .7; }
      .mod, .mod .ln_old, .mod .ln_new { color: goldenrod; }
      .del, .del .ln_old { color: red; }
      .add, .add .ln_new { color: green; }
      .token { white-space: pre; }
      .mod .token_old { background-color: red; color: white; }
      .mod .token_new { background-color: rgb(94, 167, 1); color: white; }
      .ol, .nl { width: 48%; word-break: break-all; }
</style>
  <script>
     document.addEventListener('DOMContentLoaded', () => {
     window.scrollTo(0, 0);
     const dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
     document.documentElement.classList.toggle('theme-dark', dark);
     const clk = ({target})=>{
         var n = target
         while(n && n.tagName != 'TR') n = n.parentNode
         if (n) n.style = n.style.backgroundColor? '': 'background-color: var(--tr-bg);'
     }
     document.addEventListener('click', clk)
});
  </script>
</head>
"""

if old_file:
    if total == 0:
        for i in xrange(1, ln_old_total+1):
            l = l_map[i]
            render_line(i, l, MARK_SAME, i, l)

        if option_render_html:
            print '</html>'


filename = ''
is_first_diff_header = True
is_first_hunk = None
for left, right in aligned_output:
    l_type, l_num1, l_num2, l_text, _ = left
    r_type, r_num1, r_num2, r_text, _ = right

    if l_type == 2:
        render_hunk_separator(left, filename, is_first_hunk)
        is_first_hunk = False

    elif l_type == 3 or l_type == 4:
        render_file_header(l_text)
        is_first_diff_header = False

    elif l_type == 5:
        rfilename = l_text.rsplit(None, 1)[-1]
        filename = rfilename.rsplit('/', 1)[-1]
        render_diff_header(l_text, is_first_diff_header)
        is_first_diff_header = False
        is_first_hunk = True

    elif l_type == 6:
        render_header(l_text)

    else:
        mark = None

        if l_type == 9 and r_type == 1:
            mark = MARK_ADD
        elif l_type == -1 and r_type == 9:
            mark = MARK_DEL
        elif l_type == -1 and r_type == 1:
            mark = MARK_MOD
        elif l_type == 0 and r_type == 0:
            mark = MARK_SAME
        else:
            mark = MARK_NONE

        render_line(l_num1, l_text, mark, r_num2, r_text)

# padding last parts (not included in hunk) if exists from old file
if old_file and ln_old_last > 0:             # means have been re-assigned by 'L' type meta
    n = 0
    for i in xrange(ln_old_last+1, ln_old_total+1):
        n += 1
        l = l_map[i]
        render_line(i, l, MARK_SAME, ln_new_last+n, l)

if option_render_html:
    print '</table></html>'

if option_render_json:
    print json.dumps(json_list)
