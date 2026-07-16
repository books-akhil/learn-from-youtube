# SKILL-RETROSPECT.md Format

`SKILL-RETROSPECT.md` lives in the **skill directory**, next to `SKILL.md` — not in the teaching workspace. It is the long-term memory of the skill itself — a record of friction patterns, reasoning mistakes, and design improvements discovered across teaching sessions. Because it is shared across all teaching workspaces, friction discovered while teaching one topic improves every future session.

It is **not** a conversation log, **not** a user preference file, and **not** a learner knowledge record.

## Structure

```md
# Skill Retrospective

## Active Rules

### RETRO-0001: {Short description of the design rule}
- **Problem**: {What friction was observed}
- **Evidence**: {How often / in which sessions this recurred}
- **Root Cause**: {Why the skill produced this friction}
- **Design Rule**: {The generalized rule to prevent recurrence}
- **Action**: {What was changed — or "Proposed" if not yet enacted}
- **Status**: Active

### RETRO-0002: {Short description}
...

## Superseded Rules

### RETRO-0001: {Short description}
- ...
- **Status**: Superseded by RETRO-NNNN
```

## Rules

- **Record abstractions, not incidents.** Each entry should be a reusable design rule, not a narrative of what went wrong in one session. "LaTeX escapes drop when raw strings are omitted" is a rule. "In session 3 the LaTeX broke" is a log entry.
- **Never log user preferences.** Those belong in `NOTES.md`.
- **Never log learner knowledge.** Those belong in `./learning-records/*.md`.
- **Merge similar patterns.** If a new observation matches an existing entry, update the existing entry's evidence and strengthen its design rule. Prefer updating over creating.
- **Keep it concise.** If the file grows past 30 entries, consolidate related rules into higher-level patterns. The file should stabilize, not grow linearly with sessions.
- **Supersede, don't delete.** When a rule is replaced by a better one, move it to `## Superseded Rules` with `Status: Superseded by RETRO-NNNN`. The history of how the skill evolved is useful signal.
- **Number sequentially.** Scan existing entries for the highest number and increment by one.

## When to Write

Write an entry when any of these is true:

1. **The skill made a reasoning mistake** — wrong assumptions about what the user knows, poor scoping of a notebook, incorrect concept boundaries.
2. **The skill's defaults were wrong** — a default that consistently needs overriding should become the new default.
3. **The workflow had a gap** — a step that was needed but missing from TEACH.md or SKILL.md.
4. **The same mistake recurred across sessions** — any pattern that appears twice is worth recording.
5. **An unnecessary clarification was needed** — if the user had to correct the skill on something that should have been obvious from context, the skill should learn it.

### What does _not_ qualify

- One-off user errors or typos.
- Content mistakes in a single notebook that don't indicate a systemic pattern.
- User preferences about teaching style (→ NOTES.md).
- Domain knowledge the user demonstrated (→ learning-records).
