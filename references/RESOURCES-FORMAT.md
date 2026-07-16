# RESOURCES.md Format

`RESOURCES.md` is the curated set of trusted sources for this topic. Knowledge for lessons should be drawn from here, not from parametric guesses. Wisdom comes from the communities listed here.

## Structure

```md
# {Topic} Resources

## Knowledge

- [Book: _Speech and Language Processing_ (3rd ed. draft) — Jurafsky & Martin](https://web.stanford.edu/~jurafsky/slp3/)
  Foundational NLP text, freely available. Use for: attention, transformer, and decoding chapters backing the CME295 lectures.
- [Article: "The Annotated Transformer" — Harvard NLP](https://nlp.seas.harvard.edu/annotated-transformer/)
  Line-by-line implementation of the original paper. Use for: cross-checking lesson implementations against a trusted reference.

## Wisdom (Communities)

- [r/MachineLearning](https://reddit.com/r/MachineLearning)
  High-signal subreddit with paper discussion threads. Use for: implementation critique, sanity-checking intuitions.
- Local: {university} ML reading group, Thursdays
  Use for: presenting derivations and getting real-time feedback.
```

## Rules

- **High-trust only.** Prefer primary sources, recognised experts, peer-reviewed work, and communities with strong moderation. If a resource is marketing dressed as education, leave it out.
- **Videos live in `YOUTUBE.md`, not here.** But a video's companion materials (slide PDFs, lecture notes, course sites) belong here, annotated with which video they support — they cover the visual content the transcript pipeline cannot see.
- **Annotate every entry.** A bare link is useless in three months. Add one line: what it covers and when to reach for it.
- **Group by Knowledge / Wisdom.** Mirrors the philosophy in [PEDAGOGY.md](./PEDAGOGY.md). It is fine for a resource to appear in only one group.
- **Surface gaps explicitly.** If no good resource exists for an area the mission needs, write a `## Gaps` section listing what is missing. This drives future search.
- **Prune ruthlessly.** A resource that turned out to be wrong, shallow, or off-mission should be removed, not buried. Better five sharp sources than thirty mediocre ones.
- **Record community preferences.** If the user has opted out of joining communities, note it here so future sessions don't keep proposing them.
