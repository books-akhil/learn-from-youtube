# YOUTUBE.md Format

`YOUTUBE.md` lives at the workspace root. It is the **video study queue**: the videos and playlists the user wants to learn from, plus the processing state the skill maintains for each. It is a working file, not a curation shelf — trusted non-video resources (books, articles, communities, and a video's companion slides/notes) belong in `RESOURCES.md`.

## Structure

```md
# Video Study Sources

## Stanford CME295 — Transformers & LLMs (Autumn 2025)
- URL: https://www.youtube.com/playlist?list=PLoROMvodv4rOCXd21gf0CF4xr35yINeOy
- Type: playlist
- Role: primary
- Topic: transformers
- Why: Primary lecture series for the mission. Lectures 1–6 are in scope; the rest is out of scope for now.
- Videos:

| # | Title | URL | Status | Blueprint |
|---|-------|-----|--------|-----------|
| 01 | Lecture 1 — Transformer | https://www.youtube.com/watch?v=Ub3GoFaUcds | taught | blueprints/Ub3GoFaUcds.md |
| 02 | Lecture 2 — LLM intro | https://www.youtube.com/watch?v=... | blueprinted | blueprints/<id>.md |
| 03 | Lecture 3 — Tricks | https://www.youtube.com/watch?v=... | unprocessed | — |

## How LLMs Learn (3Blue1Brown)
- URL: https://www.youtube.com/watch?v=...
- Type: video
- Role: supplementary
- Topic: transformers
- Why: Visual intuition for backpropagation, complements CME295 Lecture 1.
- Status: unprocessed
- Blueprint: —
```

## Rules

- **The user adds entries; the skill maintains them.** A user entry needs only URL and a one-line Why. The skill fills in Type, Role, Topic (matching a `LEARNING-INDEX.yaml` key where possible), the Videos table, statuses, and blueprint paths.
- **Exactly one `primary` per course document.** The primary source drives the syllabus — its order is the spine of the course. All other entries are `supplementary`: they never shape the syllabus and are blueprinted per-lesson, only when the course document flags a concept the primary covers weakly. If multiple entries could be primary, compare their titles/chapters (cheap metadata) and ask the user to pick one — never decide silently, never blend orderings.
- **Terminology conflicts across sources**: the primary's terms win; supplementary terms are recorded in `GLOSSARY.md` as *Avoid* aliases.
- **Expand playlists lazily.** Fill the Videos table only when course design first needs it, via:
  `uvx yt-dlp --flat-playlist --print "%(playlist_index)s|%(id)s|%(title)s" <playlist-url>`
  Do not blueprint every video on expansion — see BLUEPRINT-FORMAT.md for when to generate.
- **Status lifecycle**: `unprocessed` → `blueprinted` (blueprint file exists) → `taught` (a lesson covering the video's material passed the Evaluation Gate). Statuses only move forward.
- **The mission filters the playlist.** A playlist's Why line should record which parts are in scope. The course document decides teaching order and coverage — never mirror a playlist into the syllabus unfiltered.
- **Blueprint paths** point into `./blueprints/`, named by video id (`blueprints/<video-id>.md`).
- **Long videos (> ~2 hours)** get one row **per chapter-range**, not per video — same URL in each row, range in the Title column, blueprint path `blueprints/<video-id>-ch<NN>-<NN>.md`. See BLUEPRINT-FORMAT.md "Long videos" for segmentation rules:

| # | Title | URL | Status | Blueprint |
|---|-------|-----|--------|-----------|
| 01 | Ch 1–3: Intro, Tokenization | https://youtube.com/watch?v=<id> | blueprinted | blueprints/<id>-ch01-03.md |
| 02 | Ch 4–6: Attention, Transformer | https://youtube.com/watch?v=<id> | unprocessed | — |
- **Prune like RESOURCES.md**: if a video turns out to be shallow, wrong, or off-mission, remove its entry (and its blueprint) rather than letting it steer future course design.
