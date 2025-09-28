# CVS

```sh
# Initial checkout (like git clone)
cvs -d <cvsroot> checkout <module>

# Pull latest changes (like git pull)
cvs update -dP

# Edit files
nano file.c   # (or cvs edit file.c)

# See what changed
cvs diff file.c

# Add new file
cvs add newfile.c

# Commit (changes go directly to central repo)
cvs commit -m "Fixed bug in parser"
```
