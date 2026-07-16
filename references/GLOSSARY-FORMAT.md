# GLOSSARY.md Format

`GLOSSARY.md` is the canonical language for this teaching workspace. All lessons, exercises, and learning records should adhere to its terminology. Building it is itself part of learning: compressing a concept into a tight definition is evidence the user understands it.

## Structure

```md
# {Topic} Glossary

{One or two sentence description of the topic this glossary covers.}

## Terms

**Attention head**:
One independent set of query/key/value projections inside a multi-head attention layer, attending to the sequence in its own subspace.
_Avoid_: Attention unit, head matrix

**Logit**:
An unnormalized score emitted by the final linear layer, one per vocabulary token, before softmax.
_Avoid_: Probability (wrong until softmax), score

**Context window**:
The maximum number of tokens the model can attend over in one forward pass.
_Avoid_: Memory, buffer size
```

## Rules

- **Add a term only when the user understands it.** The glossary is a record of compressed knowledge, not a dictionary the user reads to learn. If the user has just been introduced to a concept, wait until they can use it correctly before promoting it here.
- **Be opinionated.** When several words exist for the same concept, pick the best one and list the rest as aliases to avoid. This is how language compresses.
- **Keep definitions tight.** One or two sentences. Define what the term IS, not what it does or how to do it.
- **Use the glossary's own terms inside definitions.** Once a term is in the glossary, prefer it everywhere — including inside other definitions. This is what makes complex terms easier to grasp later.
- **Group under subheadings** when natural clusters emerge (e.g. `## Architecture`, `## Training`). A flat list is fine when terms cohere.
- **Flag ambiguities explicitly.** If a term is used loosely in the wider field, note the resolution: "In this workspace, 'embedding' always means the token embedding vector — positional encodings are named explicitly."
- **Revise as understanding deepens.** A definition the user wrote in week one may be wrong by week six. Update in place; do not leave stale entries.
