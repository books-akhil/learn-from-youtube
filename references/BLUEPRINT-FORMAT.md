# Lecture Blueprint Format & Pipeline

A blueprint is a faithful, timestamped reconstruction of one video lecture, cached at `./blueprints/<video-id>.md`. It is generated **once per video** and consumed by TEACH.md when scoping and writing lessons, so notebooks can reuse the lecture's terminology, analogies, and sequencing and cite exact timestamps.

**Generate lazily.** Blueprint a video only when it is actually needed — when course design must scope lessons against it, or when the next notebook covers its material. Never blueprint a whole playlist up front.

## Pipeline

1. **Download captions + metadata** to a temporary directory (never the workspace):
   `uvx yt-dlp --skip-download --write-auto-subs --sub-lang en --sub-format vtt --write-info-json -o "<video-id>.%(ext)s" <url>`
2. **Clean the VTT into a timestamped transcript** with the bundled script (path relative to the skill directory):
   `python scripts/clean_vtt.py <video-id>.en.vtt 30 > transcript.txt`
   It strips cue/position tags, deduplicates the rolling caption lines (auto-subs repeat each line across cues), and merges into ~30-second buckets prefixed `[MMM:SS]`.
3. **Pull chapters and description** from the `.info.json`. Chapter markers anchor the outline's top level; the description often lists companion materials.
4. **Write the blueprint** from transcript + chapters only. Record what *this lecture* teaches, in its own words and examples — do not substitute textbook-standard phrasings or examples the lecturer did not use. (Plausible-but-unsaid substitutions are the failure mode this format exists to prevent.)
5. Save to `./blueprints/<video-id>.md` and update the video's row in `YOUTUBE.md` (`Status: blueprinted`, blueprint path).

## Blueprint structure

```md
# Lecture Blueprint — <lecture title>

**Video**: link · channel · duration · recording date
**Instructors**: names, relevant background
**Companion materials**: textbook, slides, sites named in the lecture/description

1. Learning Objectives — what a student can *do* after this lecture
2. Prerequisite Knowledge — stated explicitly vs. assumed implicitly
3. Pedagogical Architecture — running examples, sequencing strategy (e.g. motivation-by-failure), recurring devices
4. Hierarchical Outline with Timestamps — sections to sub-minute granularity: concepts, definitions,
   formulas, worked examples, Q&A moments, and the transition INTO each section
5. Complete Concept Inventory — explicitly taught / implicit or assumed / explicitly deferred
6. Key Intuitions, Analogies & Mental Models — table: concept → device used
7. Misconceptions Explicitly Addressed
8. Definitions & Formulas — exactly as stated in-lecture
9. Exercises & Assessment Moments — embedded quizzes, planted questions and where they pay off
10. Takeaways — the lecture's own summary spine
11. Transition Logic — table: from → to, why the order is forced
```

## Long videos (> ~2 hours)

Treat a long video like a playlist, with chapters as the videos:

1. **Segment by chapters.** The chapter list is already in the metadata. Group chapters into ranges that each hold roughly one lesson's worth of material (the same scoping unit TEACH.md uses). No chapters → fall back to fixed ~60–90 minute segments and note in the blueprint header that boundaries are arbitrary (transition logic may span segments).
2. **One queue row per chapter-range** in `YOUTUBE.md` (see YOUTUBE-FORMAT.md), each with its own status and blueprint path.
3. **Download captions once, slice per range.** The transcript is timestamped and chapters give the cut points — never re-download for later segments. Cache the full cleaned transcript in the temporary directory while segmenting.
4. **Blueprint per range, lazily**, to `./blueprints/<video-id>-ch<NN>-<NN>.md` (or `-seg<NN>` for fixed segments). Each blueprint covers only its range but should name what the ranges before/after cover (one line each) so lessons can reference continuity.
5. **Mature workspaces**: blueprint generation for a segment may be delegated to a subagent (same pattern as SKILL.md Step 1) to keep the main context clean.

## Caveats

- **Auto-caption quality varies.** If the transcript is rough (heavy mis-transcription, missing segments), note it in the blueprint header so lessons treat details with suspicion.
- **Visual-only content is invisible** to this pipeline (slides, board work, animations). Check `RESOURCES.md` for companion slides/notes and fold them in; if none exist, flag the gap both in the blueprint header and in `RESOURCES.md` under `## Gaps`.
- **Spoken math is lossy.** Formulas in section 8 should be reconstructed conservatively; when the transcript is ambiguous, mark the formula as inferred.
