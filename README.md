# UnifiedDiffOutputParser
A simple yet effective python parser for unified diff file


# How to use it

```
./udiff_parser.py d.diff
```
And the result just been dumped right in file ```d.json```

# Do some modification

* make some modification on file 1, 2
* generate the diff file
```
./diff.py -u -l0 1 2 > d.diff
```
* parse and see the diff result
```
./udiff_parser.py d.diff
```

The output of ```./udiff_parser.py``` if very simple and easy to be modifed to fit your need, give it a try!
