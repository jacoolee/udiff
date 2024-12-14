#! /usr/bin/env python
# -*- coding: utf-8 -*-

# https://en.wikipedia.org/wiki/Diff#Unified_format
# https://www.gnu.org/software/diffutils/manual/html_node/Detailed-Unified.html

from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
import re

if len(sys.argv) > 1:
    diff_file = sys.argv[1]
    ls = open(diff_file, "r").readlines()
else:
    ls = sys.stdin

r = []
for l in ls:
    l = l.replace('\n', '')

    if l.startswith('diff '):
        r.append([5, None, None, l, None])
        continue

    if l.startswith('index '):
        r.append([6, None, None, l, None])
        continue

    if l.startswith('---'):
        r.append([3, None, None, l, None])
        continue

    if l.startswith('+++'):
        r.append([4, None, None, l, None])
        continue

    if l.startswith('@@'):
        start, start_count, end, end_count = re.match('@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@', l).groups()
        ln_old = int(start)
        ln_new = int(end)

        start_count = int(start_count or 1)
        end_count = int(end_count or 1)

        r.append([2, ln_old, ln_new, start_count, end_count])
        continue

    if l.startswith(' '):
        r.append([0, ln_old, ln_new, l[1:], None])
        ln_old = ln_old + 1
        ln_new = ln_new + 1
        continue

    if l.startswith('-'):
        r.append([-1, ln_old, None, l[1:], None])
        ln_old = ln_old + 1
        continue

    if l.startswith('+'):
        r.append([1, None, ln_new, l[1:], None])
        ln_new = ln_new + 1
        continue

    # else, ignore

print json.dumps(r)
