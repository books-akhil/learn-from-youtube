---
name: learn-from-youtube
description: Turn YouTube videos or playlists into interactive marimo lesson notebooks, taught as a stateful tutor with persistent learning records. Use when the user wants to learn a subject from video lectures, study a YouTube course or playlist, or continue lessons in an existing teaching workspace. Optionally provide a 'Topic'; if omitted, the next lesson is inferred from the course document and the user's zone of proximal development.
disable-model-invocation: true
---

## Quick Start

First time: create a workspace directory, drop video/playlist links into `YOUTUBE.md` (just a URL and a one-line why each), invoke this skill from that directory, and answer the mission questions. Every later session: invoke the skill again from the same directory (optionally with a Topic) — it resumes from the workspace state.

## Two Directories

This skill separates its machinery from the learning state:

- **Skill directory** — where this SKILL.md lives. Holds the static teaching machinery (`references/`) and `SKILL-RETROSPECT.md`, the skill's own long-term memory. Shared across all teaching workspaces.
- **Teaching workspace** — the directory the user invoked the skill from. Holds all per-topic learning state. One mission per workspace.

## Workspace Files

- `MISSION.md`: User's core motivation. Format: [references/MISSION-FORMAT.md](./references/MISSION-FORMAT.md).
- `RESOURCES.md`: Contextual knowledge. Format: [references/RESOURCES-FORMAT.md](./references/RESOURCES-FORMAT.md).
- `GLOSSARY.md`: Canonical vocabulary. Format: [references/GLOSSARY-FORMAT.md](./references/GLOSSARY-FORMAT.md).
- `NOTES.md`: Active syllabus, environment, and user preferences. Template: [references/NOTES-TEMPLATE.md](./references/NOTES-TEMPLATE.md).
- `LEARNING-INDEX.yaml`: Central index mapping topics to specific learning records. Format: [references/LEARNING-INDEX-FORMAT.md](./references/LEARNING-INDEX-FORMAT.md).
- `YOUTUBE.md`: Video study queue — videos/playlists to learn from, with processing status. Format: [references/YOUTUBE-FORMAT.md](./references/YOUTUBE-FORMAT.md).
- `./blueprints/*.md`: Cached lecture blueprints extracted from videos, one per video id. Format & pipeline: [references/BLUEPRINT-FORMAT.md](./references/BLUEPRINT-FORMAT.md).
- `./learning-records/*.md`: Architectural decision records for learning. Format: [references/LEARNING-RECORD-FORMAT.md](./references/LEARNING-RECORD-FORMAT.md).
- `./lessons/*.py`: The **lessons** (marimo notebooks). **Naming**: Match course syllabus numbering (`Part 1.1` → `0101-<name>.py`).
- `pyproject.toml` + `uv.lock`: The uv project manifest — the single source of truth for lesson dependencies. Managed exclusively via `uv add` / `uv remove`, never edited by hand.

**Missing-file rule**: If any workspace file other than `MISSION.md`, `NOTES.md`, and `pyproject.toml` is missing, skip it and continue — Step 0 bootstraps those three, the rest are created lazily by Step 4.

## Step 0 — Bootstrap

1. If `MISSION.md` does not exist:
   - If `YOUTUBE.md` exists, first fetch cheap metadata for its entries — titles, descriptions, chapter lists (`uvx yt-dlp --flat-playlist --print "%(playlist_index)s|%(id)s|%(title)s" <playlist-url>` for playlists; `uvx yt-dlp --skip-download --print "%(title)s\n%(description)s" <url>` for single videos). **No captions, no blueprints yet.**
   - Interview the user to create `MISSION.md`, grounding the questions in what the videos cover ("this playlist spans X→Y — which parts matter to you, and why?"). Format: [references/MISSION-FORMAT.md](./references/MISSION-FORMAT.md). Do not proceed until `MISSION.md` exists. **Fast path**: if the queue is a single video with an obvious topic, cap the interview at 2–3 questions — a few-line mission beats a stalled start.
2. If `pyproject.toml` does not exist, make the workspace uv-managed: run `uv init` (delete any sample `main.py` it generates), then `uv add marimo` as the baseline dependency. All further dependencies are added in Step 2 — do not guess frameworks here.
3. If `NOTES.md` does not exist, instantiate it from [references/NOTES-TEMPLATE.md](./references/NOTES-TEMPLATE.md).

## Step 1 — Resolve Topic & State

**Topic**: Use the Topic the user provided. If none was given, infer one: read the course document (if any) and pick the next uncovered syllabus item within the user's zone of proximal development (see [references/PEDAGOGY.md](./references/PEDAGOGY.md)). State the inferred Topic to the user before proceeding.

**Context gathering** — match the effort to the workspace's size:

- **Small workspace** (the Topic's block in `LEARNING-INDEX.yaml` lists fewer than 5 records, or the index is missing): Read the Topic's learning records and `RESOURCES.md` directly. Do not spawn subagents — the cold-start cost outweighs the benefit.
- **Mature workspace** (5+ records for the Topic): Use subagents to summarize heavy context, keeping your main context window pristine:
  1. **Knowledge Subagent**: Spawn a subagent to read `LEARNING-INDEX.yaml` and the requested **Topic**. It must locate the specific records for that topic, read only those files in `./learning-records/`, and return a condensed "Knowledge Brief". *Failure Handling*: If a record is missing/empty, ignore it but report it for pruning. If the index is unparseable, warn the user but proceed with zero prior knowledge.
  2. **Resource Subagent**: Only if `RESOURCES.md` exceeds ~100 lines, spawn a subagent to read it plus the **Topic** and return a condensed "Resource Brief" of applicable links/materials. Otherwise read it directly.

**Synthesis**: You (the main agent) read `MISSION.md`, `NOTES.md`, `GLOSSARY.md` (workspace), and `SKILL-RETROSPECT.md` (skill directory), and synthesize them with the gathered context. Synthesis is complete when you have a unified context ready for course resolution.

## Step 2 — Resolve Course & Dependencies

**Course**: Does `NOTES.md` reference a course document, and does that file exist on disk?

- **Yes** → Read the referenced course document.
- **No, and the only in-scope source is a single video (or one chapter-range)** → **Fast path**: skip course design. Blueprint that video (per [references/BLUEPRINT-FORMAT.md](./references/BLUEPRINT-FORMAT.md)) and use the blueprint as the course document — reference it from `NOTES.md`; lesson cell budgets follow the blueprint's scope rather than the 35–40 default.
- **No** → Read [references/PEDAGOGY.md](./references/PEDAGOGY.md). If `YOUTUBE.md` lists videos covering the mission, derive the course document from the **single `Role: primary` source** (per [references/YOUTUBE-FORMAT.md](./references/YOUTUBE-FORMAT.md)): expand it, filter it through `MISSION.md` — never mirror it unfiltered — and blueprint only the video(s) needed to scope the early lessons (per [references/BLUEPRINT-FORMAT.md](./references/BLUEPRINT-FORMAT.md)). If no entry is marked primary and more than one could be, ask the user to pick one — never blend orderings from multiple sources. Supplementary entries never shape the syllabus; note in the course document where a supplementary video should back up a weakly-covered concept. Otherwise design the course from scratch, aligned with `MISSION.md` and the user's zone of proximal development. Save it to the workspace. Update `NOTES.md` to reference the new course document.

**Dependencies**: With the course document in hand, derive the dependencies the upcoming lessons need from `MISSION.md` and the syllabus (e.g. `numpy`, `matplotlib`, `torch`). Compare against the dependencies already in `pyproject.toml`. If any are missing, present the proposed list to the user with a one-line reason per dependency and ask for confirmation — the user may swap alternatives (e.g. JAX instead of torch) or defer some. Install the approved set with `uv add`. Only propose dependencies the syllabus actually requires soon; do not front-load the whole course's stack. Proceed to Step 3.

## Step 3 — Generate Notebook

Read [references/TEACH.md](./references/TEACH.md) and follow it to generate the notebook. This step is complete only when the notebook executes cleanly and passes the Evaluation Gate defined in `references/TEACH.md`.

## Step 4 — Post-Generation Checklist

After the notebook passes the Evaluation Gate in references/TEACH.md, execute these updates:

1. **Learning Records**: If the notebook introduced a concept the user demonstrably understood (not just covered), create a new learning record. Format: [references/LEARNING-RECORD-FORMAT.md](./references/LEARNING-RECORD-FORMAT.md).
2. **Learning Index**: If you created a new learning record, append its filename to the appropriate topic block in `LEARNING-INDEX.yaml` at the workspace root (create the file if it does not exist). Additionally, prune any dead references (files that were missing or empty) discovered during context gathering. Format: [references/LEARNING-INDEX-FORMAT.md](./references/LEARNING-INDEX-FORMAT.md).
3. **Glossary**: If the notebook introduced or refined canonical terms, append them to `GLOSSARY.md`. Create the file if it does not exist. Format: [references/GLOSSARY-FORMAT.md](./references/GLOSSARY-FORMAT.md).
4. **Video Queue**: If the lesson drew on video blueprints, update the corresponding rows in `YOUTUBE.md`: record any newly created blueprint paths and advance statuses (`blueprinted` → `taught` for videos whose material the lesson covered). Format: [references/YOUTUBE-FORMAT.md](./references/YOUTUBE-FORMAT.md).
5. **Skill Retrospective**: Analyze the session for friction originating from the skill itself. Update `SKILL-RETROSPECT.md` **in the skill directory** (not the workspace — it is shared across all workspaces) with any new or updated design rules. Create the file if it does not exist. Format: [references/RETROSPECT-FORMAT.md](./references/RETROSPECT-FORMAT.md).

## Step 5 — Done

Report to the user: the notebook filename, concepts covered (start → stop), and any state files created or updated. Ask if they want to continue to the next lesson.
