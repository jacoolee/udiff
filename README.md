# Udiff - View diff content side by side

![](./screenshots/terminal.png)

![](./screenshots/html.png)

```
$ ./udiff 36531bd f8e784f
$ ENV_HTML=1 ./udiff 36531bd f8e784f > /tmp/udiff.output.html; open /tmp/udiff.output.html
```

---

## Run directly

```
$ ./udiff
```

## For Daily Use

```
# load udiff.source file in your ~/.bashrc

source {YOUR_UDIFF_DIRPATH}/udiff.source
```

Then, you can use `d` directly, and `D` to export html

```
$ d
$ D # export as html
```

## View git log

```
$ git log
COMMIT_ID_C hello
COMMIT_ID_B some modify here
COMMIT_ID_A init

$ udiff COMMIT_ID_A COMMIT_ID_B
$ ENV_HTML=1 udiff COMMIT_ID_A COMMIT_ID_B
```

## Diff and view any files

Check out [./example](./example)
