#! /usr/bin/env python2
# -*- coding: utf-8 -*-

# consult by Google AI Mode

import re

class RawSequenceMatcher:
    """
    A 100% dependency-free exact replica of Python's difflib.SequenceMatcher
    using the Ratcliff-Obershelp longest common contiguous block algorithm.
    """
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
        self._matching_blocks = None

    def find_longest_match(self, alo, ahi, blo, bhi):
        """
        Scans window slices to pinpoint the absolute longest matching block
        of characters shared contiguously between s1 and s2.
        """
        best_i, best_j, best_size = alo, blo, 0

        # Accelerate lookups by index mapping the target window characters of s2
        j_indices = {}
        for j in range(blo, bhi):
            c = self.s2[j]
            if c not in j_indices:
                j_indices[c] = []
            j_indices[c].append(j)

        for i in range(alo, ahi):
            c = self.s1[i]
            if c in j_indices:
                for j in j_indices[c]:
                    # Match contiguous sequence expansion
                    k = 0
                    while (i + k < ahi and
                           j + k < bhi and
                           self.s1[i + k] == self.s2[j + k]):
                        k += 1

                    if k > best_size:
                        best_i, best_j, best_size = i, j, k

        return best_i, best_j, best_size

    def get_matching_blocks(self):
        """
        Recursively processes split sub-segments (left and right of matches)
        to identify all matching blocks, sorting them sequentially.
        """
        if self._matching_blocks is not None:
            return self._matching_blocks

        matching_blocks = []
        # Queue schema tracks: (alo, ahi, blo, bhi) bounding boxes
        queue = [(0, len(self.s1), 0, len(self.s2))]

        while queue:
            alo, ahi, blo, bhi = queue.pop(0)
            i, j, k = self.find_longest_match(alo, ahi, blo, bhi)

            if k > 0:
                matching_blocks.append((i, j, k))
                # Recursively look left of the matching block anchor
                if alo < i and blo < j:
                    queue.append((alo, i, blo, j))
                # Recursively look right of the matching block anchor
                if i + k < ahi and j + k < bhi:
                    queue.append((i + k, ahi, j + k, bhi))

        # Sort sequentially to conform with standard difflib behavior
        matching_blocks.sort(key=lambda x: x[0])
        # Append standard final sentinel block configuration
        matching_blocks.append((len(self.s1), len(self.s2), 0))

        self._matching_blocks = matching_blocks
        return self._matching_blocks

    def ratio(self):
        """
        Returns the similarity score as a float multiplier between 0.0 and 1.0.
        Formula: 2.0 * sum(match_lengths) / (len(s1) + len(s2))
        """
        total_len = len(self.s1) + len(self.s2)
        if not total_len:
            return 1.0

        blocks = self.get_matching_blocks()
        matches = sum(k for i, j, k in blocks)
        return (2.0 * matches) / total_len

def strip_comment_symbols(text):
    """
    Removes common code comment characters from the start of a line
    to ensure commented code blocks align perfectly line-by-line.
    """
    s = text.lstrip()
    while True:
        if s.startswith("//"):
            s = s[2:].lstrip()
        elif s.startswith("#"):
            s = s[1:].lstrip()
        elif s.startswith("--"):
            s = s[2:].lstrip()
        elif s.startswith("/*"):
            s = s[2:].lstrip()
        elif s.endswith("*/"):
            s = s[:-2].rstrip()
        else:
            break
    return s

def is_similar(left_text, right_text, threshold=0.60):
    """
    Determines if two lines match structurally based on character similarity,
    completely ignoring all spaces, tabs, and indentation.
    """
    if left_text == right_text:
        return True

    # Isolate textual content away from formatting junk
    s1 = "".join(c for c in strip_comment_symbols(left_text) if c not in (' ', '\t', '\n', '\r'))
    s2 = "".join(c for c in strip_comment_symbols(right_text) if c not in (' ', '\t', '\n', '\r'))

    # Run the exact SequenceMatcher algorithm clone
    matcher = RawSequenceMatcher(s1, s2)
    return matcher.ratio() >= threshold

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

import sys
import json

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
aligned_output = render_diff_side_by_side(diff_list)

print json.dumps(aligned_output)
