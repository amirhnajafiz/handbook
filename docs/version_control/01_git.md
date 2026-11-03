# Git

## Quick Description (QD)

**Git** is a free and open source distributed version control system. Every clone of a repository contains the full history, so most operations (commit, diff, log, branch) are local and fast, and there is no required central server (though teams usually use one, such as GitHub, as a shared remote).

### Key Concepts

- **Snapshots, not diffs:** Each commit records a snapshot of the whole project, identified by a SHA hash. Unchanged files are stored as links to the previous identical object.
- **Three areas:** The *working tree* (your files), the *staging area* or index (what goes into the next commit), and the *repository* (the `.git` directory with the history).
- **Branches:** Lightweight movable pointers to commits. `HEAD` points to the branch (or commit) you currently have checked out.
- **Remotes:** Other copies of the repository (e.g., `origin`). You `fetch` and `pull` changes from them and `push` yours to them.
- **Merge:** Combines the histories of two branches, creating a merge commit when they have diverged.

## Installation

On Debian/Ubuntu:

```bash
sudo apt install git
```

On macOS (it also ships with the Xcode command line tools):

```bash
brew install git
```

Then set your identity, which is stored in every commit you make:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Useful Tips/Commands (UToC)

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

Show changes between commits, between a commit and the working tree, etc.:

```bash
git diff
```

List, create, or delete branches:

```bash
git branch
```

Switch to another branch (`git switch` is the newer, clearer command; `git checkout <branch>` still works):

```bash
git switch <branch>
```

Create and switch to a new branch:

```bash
git switch -c <new-branch>
```

Merge another branch into the current branch:

```bash
git merge <branch>
```

Fetch from a remote and integrate it into the current branch (`git fetch` followed by `git merge`):

```bash
git pull
```

Upload your local commits to a remote repository:

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

Reset the current HEAD to the specified state (`--hard` also discards uncommitted changes in the working tree, so use it with care):

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

Apply the most recently stashed changes and remove them from the stash:

```bash
git stash pop
```

Get the list of tags:

```bash
git tag
```

Create a new lightweight tag (use `git tag -a v0.0.1 -m "message"` for an annotated one):

```bash
git tag v0.0.1
```

Push tags:

```bash
git push --tags
```

## Examples (e.g.,)

_Nothing here yet._

## References

- [Git documentation](https://git-scm.com/doc)
- [Pro Git book](https://git-scm.com/book/en/v2)
- [A tutorial introduction to Git](https://git-scm.com/docs/gittutorial)
