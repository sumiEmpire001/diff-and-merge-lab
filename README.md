# Diff and Merge Lab

A Python standard-library demonstration of unified text diffs and conservative three-way line merging. Produces unified diffs using `difflib` and merges simple nonoverlapping edits against a common base. Ambiguous or overlapping edits produce a conflict rather than silently choosing a version.

## Usage

```bash
python merge_lab.py diff examples/base.txt examples/ours.txt
python merge_lab.py merge examples/base.txt examples/ours.txt examples/theirs.txt
```

The merge command prints JSON with `text` and `conflicts`, exiting with status 1 on conflict.

## Tests

```bash
python -m unittest discover -s tests -v
```

Eight tests run on Python 3.10, 3.12 and 3.13 via GitHub Actions.

## Limitations

This is an educational line-based merger, **not a replacement for Git's merge engine**. It does not handle binary files, renames, moved blocks, all insertion ambiguities, or complex overlapping hunks. Back up important files before using the output.
