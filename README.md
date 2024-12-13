```
https://www.gnu.org/software/diffutils/manual/html_node/Example-Unified.html
https://www.gnu.org/software/diffutils/manual/html_node/Detailed-Unified.html
https://en.wikipedia.org/wiki/Diff#Unified_format

----------------------------------------------------------------

diff -u lao tzu > lao.tzu.diff

--- lao	2024-12-05 22:37:08
+++ tzu	2024-12-06 14:44:00
@@ -1,7 +1,6 @@
-The Way that can be told of is not the eternal Way;
-The name that can be named is not the eternal name.
 The Nameless is the origin of Heaven and Earth;
-The Named is the mother of all things.
+The named is the mother of all things.
+
 Therefore let there always be non-being,
   so we may see their subtlety,
 And let there always be being,
@@ -9,3 +8,6 @@
 The two are the same,
 But after they are produced,
   they have different names.
+They both may be called deep and profound.
+Deeper and more profound,
+The door of all subtleties!

----------------------------------------------------------------

./parse.py lao.tzu.diff lao.tzu.json

      --- lao	2024-12-05 22:37:08
      +++ tzu	2024-12-06 14:44:00
      @@ -1,7 +1,6 @@
ln_old: 1 ln_new: 1
01    -The Way that can be told of is not the eternal Way;
02    -The name that can be named is not the eternal name.
03 01  The Nameless is the origin of Heaven and Earth;
04    -The Named is the mother of all things.
   02 +The named is the mother of all things.
   03 +
05 04  Therefore let there always be non-being,
06 05    so we may see their subtlety,
07 06  And let there always be being,
      @@ -9,3 +8,6 @@
ln_old: 9 ln_new: 8
09 08  The two are the same,
10 09  But after they are produced,
11 10    they have different names.
   11 +They both may be called deep and profound.
   12 +Deeper and more profound,
   13 +The door of all subtleties!

----------------------------------------------------------------

./gen_new_by_old_file_and_diff_json_file.py lao lao.tzu.json > tzu.gen

diff tzu tzu.gen

----------------------------------------------------------------

./view.py lao lao.tzu.json # same as `./view.py lao lao.tzu.json --txt`

./view.py lao lao.tzu.json --html > ./lao.tzu.view.html

```
