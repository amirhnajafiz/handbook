# sed

## Quick Description (QD)

To replace all occurrences of a string within a file in Linux, the `sed` (stream editor) command is commonly used.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

To replace all occurrences of "old-string" with "new-string" in a file named `yourfile.txt`, use the following command:

```bash
sed -i 's/old-string/new-string/g' yourfile.txt
```

Explanation:

- `sed`: the command for the stream editor.
- `-i`: this option specifies that the changes should be made "in place," meaning the original file will be modified directly. Without this, `sed` would print the modified content to standard output. (This is GNU `sed`; BSD/macOS `sed` requires a suffix argument, e.g., `sed -i '' ...`.)
- `'s/old-string/new-string/g'`: this is the substitution command.
  - `s`: indicates the substitute command.
  - `/old-string/`: the regular expression representing the string to be found. Characters like `.`, `*` and `[` are special in it and must be escaped with a backslash to match literally.
  - `/new-string/`: the string that will replace the found string (`&` stands for the whole match).
  - `g`: the "global" flag, which ensures that all occurrences of "old-string" on each line are replaced, not just the first one.
- `yourfile.txt`: the name of the file you want to modify.

If the strings contain `/`, use another delimiter, e.g., `s|/old/path|/new/path|g`. To keep a backup, use `-i.bak`.

## Examples (e.g.,)

_Nothing here yet._

## References

- [GNU sed manual](https://www.gnu.org/software/sed/manual/sed.html)
