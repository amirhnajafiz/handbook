# CVS

## Quick Description (QD)

**CVS (Concurrent Versions System)** is an older, centralized version control system. It records the history of source files and lets several developers work on the same files at the same time. It is largely replaced by [Git](01_git.md), but it is still found in legacy projects.

### Key Concepts

- **Repository:** The single central place (selected by the `CVSROOT`, e.g., via `-d <cvsroot>`) that holds the history of every file. It can be local or accessed over a network.
- **Module:** A named directory or set of files in the repository that you check out.
- **Working copy:** The files you check out and edit. Unlike Git, you do not get the full history locally.
- **Per-file revisions:** Each file has its own revision numbers (1.1, 1.2, ...) instead of project-wide commits, and a commit is not atomic across files.
- **Copy-modify-merge:** Several developers edit their own copies. `cvs update` merges changes from the repository into your copy, and you resolve any conflicts before you `commit`.
- **Tags and branches:** Used to mark a release or to develop in parallel, applied per file.

## Installation

On Debian/Ubuntu:

```bash
sudo apt install cvs
```

On macOS:

```bash
brew install cvs
```

## Useful Tips/Commands (UToC)

Initial checkout (similar to `git clone`, but it only fetches the latest revision):

```bash
cvs -d <cvsroot> checkout <module>
```

Pull the latest changes (similar to `git pull`). `-d` creates directories that were added in the repository and `-P` prunes empty directories:

```bash
cvs update -dP
```

Edit files with any editor (`cvs edit file.c` is only needed when the repository uses watches, to tell other developers you are editing):

```bash
nano file.c
```

See what changed:

```bash
cvs diff file.c
```

Add a new file (it is only added to the repository at the next `cvs commit`):

```bash
cvs add newfile.c
```

Commit (changes go directly to the central repository):

```bash
cvs commit -m "Fixed bug in parser"
```

## Examples (e.g.,)

_Nothing here yet._

## References

- [CVS - Open Source Version Control](https://www.nongnu.org/cvs/)
- [Version Management with CVS (manual)](https://www.gnu.org/software/trans-coord/manual/cvs/cvs.html)
