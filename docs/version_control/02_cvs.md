# CVS

Initial checkout (like git clone):

```bash
cvs -d <cvsroot> checkout <module>
```

Pull latest changes (like git pull):

```bash
cvs update -dP
```

Edit files:

```bash
nano file.c   # (or cvs edit file.c)
```

See what changed:

```bash
cvs diff file.c
```

Add new file:

```bash
cvs add newfile.c
```

Commit (changes go directly to central repo):

```bash
cvs commit -m "Fixed bug in parser"
```
