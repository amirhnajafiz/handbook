# Git

Initialize a new Git repository:

```bash
git init
```

Clone a repository into a new directory:

```bash
git clone <repository-url>
```

Show the working tree status:

```bash
git status
```

Add file contents to the staging area:

```bash
git add <file>
```

Add all changes in the current directory to the staging area:

```bash
git add .
```

Record changes to the repository with a message:

```bash
git commit -m "commit message"
```

Show commit logs:

```bash
git log
```

Show changes between commits, commit and working tree, etc.:

```bash
git diff
```

List, create, or delete branches:

```bash
git branch
```

Switch to another branch:

```bash
git checkout <branch>
```

Create and switch to a new branch:

```bash
git checkout -b <new-branch>
```

Merge another branch into the current branch:

```bash
git merge <branch>
```

Fetch from and integrate with another repository or a local branch:

```bash
git pull
```

Update remote refs along with associated objects:

```bash
git push
```

Show remote connections:

```bash
git remote -v
```

Download objects and refs from another repository:

```bash
git fetch
```

Reset current HEAD to the specified state:

```bash
git reset --hard <commit>
```

Remove files from the working tree and from the index:

```bash
git rm <file>
```

Stash the changes in a dirty working directory:

```bash
git stash
```

Apply the most recently stashed changes and remove them:

```bash
git stash pop
```

Get the list of tags:

```bash
git tag
```

Create a new tag:

```bash
git tag v0.0.1
```

Push tags:

```bash
git push --tags
```
