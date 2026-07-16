# LEARNING-INDEX.yaml Format

`LEARNING-INDEX.yaml` lives at the **workspace root**. It acts as a central registry mapping broad topics to specific learning records. This prevents the agent from needing to load all historical records, avoiding context explosion. Create it lazily — when the first learning record is written.

## Structure

The file is a standard YAML dictionary where the top-level keys are topics. Each topic has a `records` list containing the filenames of associated learning records. Filenames follow the learning-record naming scheme (`NNNN-slug.md`, see [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md)).

```yaml
topics:
  linear_algebra:
    records:
      - 0001-la-vectors.md
      - 0002-la-matrices.md
      - 0005-la-eigen.md
  pinns:
    records:
      - 0003-pinn-basics.md
```

## Updating the Index

When a new learning record is generated (Step 4 of `SKILL.md`):
1. Determine the closest matching `topic` for the new record. If a suitable topic does not exist, create a new top-level topic key.
2. Append the new learning record's filename to the `records` list under that topic.
3. Keep the list flat; do not include paths (e.g., use `0004-record-name.md`, not `./learning-records/0004-record-name.md`).

## Failure Handling & Pruning
If context gathering reports that a file listed in the index is missing or empty, you must automatically delete that filename from the `records` list to self-heal the index.
