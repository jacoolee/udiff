#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import re

def is_similar(left_text, right_text):
    """
    Determines if two rows are structurally similar modifications.
    """
    if left_text == right_text:
        return True
    return left_text.strip().lower() == right_text.strip().lower() and len(left_text.strip()) > 0


def align_buffer(deletion_buffer, addition_buffer):
    """
    Applies the LCS algorithm to align a block of deletions and additions.
    Returns a list of paired lines: (left_line_data, right_line_data)
    """
    m, n = len(deletion_buffer), len(addition_buffer)
    
    # 1. Build the DP matrix for LCS tracking
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Index 3 contains the actual string content
            if is_similar(deletion_buffer[i - 1][3], addition_buffer[j - 1][3]):
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    # 2. Backtrack to align parallel rows
    aligned = []
    i, j = m, n
    empty_left = [9, None, None, '', '']
    empty_right = [9, None, None, '', '']
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and is_similar(deletion_buffer[i - 1][3], addition_buffer[j - 1][3]):
            aligned.insert(0, (deletion_buffer[i - 1], addition_buffer[j - 1]))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            aligned.insert(0, (empty_left, addition_buffer[j - 1]))
            j -= 1
        else:
            aligned.insert(0, (deletion_buffer[i - 1], empty_right))
            i -= 1
            
    return aligned


def render_diff_side_by_side(diff_list):
    """
    Processes a sequential diff stream and returns an aligned list of paired lines.
    Each output item is a tuple: (left_line_data, right_line_data)
    """
    aligned_output = []
    deletion_buffer = []
    addition_buffer = []
    empty_right = [9, None, None, '', '']

    def flush_buffers():
        if deletion_buffer or addition_buffer:
            aligned_blocks = align_buffer(deletion_buffer, addition_buffer)
            aligned_output.extend(aligned_blocks)

            # deletion_buffer.clear()
            # addition_buffer.clear()

            deletion_buffer[:] = []
            addition_buffer[:] = []

    for item in diff_list:
        line_type = item[0]
        
        if line_type == -1: # Deletion
            deletion_buffer.append(item)
        elif line_type == 1: # Addition
            addition_buffer.append(item)
        else:
            # Context (0), Hunk headers (2), File headers (3, 4) flush any pending edits
            flush_buffers()
            
            if line_type == 0: # Context
                aligned_output.append((item, item))
            else: 
                # Structural/Meta line types span full width (leave right empty)
                aligned_output.append((item, empty_right))
                
    # Final flush at end of data stream
    flush_buffers()
    
    return aligned_output

# SEP ################################################################

if len(sys.argv) > 1:
    diff_file = sys.argv[1]
    ls = open(diff_file, "r").readlines()
else:
    ls = sys.stdin

r = []
for l in ls:
    l = l.replace('\n', '')

    if l.startswith('diff '):
        r.append([5, None, None, l, ''])
        continue

    if l.startswith('index '):
        r.append([6, None, None, l, ''])
        continue

    if l.startswith('---'):
        r.append([3, None, None, l, ''])
        continue

    if l.startswith('+++'):
        r.append([4, None, None, l, ''])
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
        r.append([0, ln_old, ln_new, l[1:], ''])
        ln_old = ln_old + 1
        ln_new = ln_new + 1
        continue

    if l.startswith('-'):
        r.append([-1, ln_old, '', l[1:], ''])
        ln_old = ln_old + 1
        continue

    if l.startswith('+'):
        r.append([1, None, ln_new, l[1:], ''])
        ln_new = ln_new + 1
        continue

    # else, ignore


# SEP ################################################################

diff_list = r
# print diff_list, '\n'

print json.dumps(diff_list)


# SEP ################################################################

# def _fls(txt=None):
#     option_width = 50
#     max_len = option_width
#     _txt = txt or ''

#     if len(_txt) < max_len:
#         return _txt + ' '*(max_len-len(_txt))
#     return _txt[0:max_len]

# SEP ################################################################

# aligned_output = render_diff_side_by_side(diff_list)

# for left, right in aligned_output:
#     l_type, l_num1, l_num2, l_text, _ = left
#     r_type, r_num1, r_num2, r_text, _ = right

#     if l_type in [2,3,4]:
#         print left, right, '\n'
#         continue

#     # print
#     # print '> ', left, right
#     print "%2s:%2s %5s %s %5s %s"%(l_type, r_type, l_num1 or '', _fls(str(l_text)), r_num2 or '', _fls(str(r_text)))
