# Notebook Generation Engine

Read and apply these rules when generating a notebook. The router (SKILL.md) resolves the course document and workspace state before invoking this file.

## Prerequisites
- Write the notebook in marimo's file format: a pure-Python file with `import marimo`, `app = marimo.App()`, one `@app.cell`-decorated function per cell, and `if __name__ == "__main__": app.run()` — verify it executes with `uv run`. If a skill named `marimo-notebook` is available in this session, invoke it first and follow its guidance instead.

## Philosophy
- **System 2 Exercise**: Start with raw tensor/array implementations from first principles. Introduce high-level library abstractions only as a reward.
- **Design Tree (Domain Translation)**: Emulate a mathematician exploring an open problem. Treat the path as a search tree driven by perspective shifts. Translate problems into different domains (e.g., spatial metaphors) rather than brute-forcing abstract algebra. Keep failed branches visible to motivate perspective shifts. A branch is a cell sequence that tries one approach; when it hits a dead end, label it `# DEAD END:` with a one-line explanation before trying the next approach.
- **Reactivity**: Expose every core hyperparameter as an interactive `mo.ui` widget wired directly into the computation.

## Execution Rules
- **Course Architect**: Establish the notebook's scope before writing any cells:
  1. Read the course document identified by the router and the **previous notebook**. If no previous notebook exists (first lesson), begin at the start of the course document.
  2. If `YOUTUBE.md` maps a source video to the syllabus items in scope, also read that video's blueprint from `./blueprints/` — generate it first per `references/BLUEPRINT-FORMAT.md` if missing.
  3. If the course document flags a supplementary video for a concept in scope, blueprint only the relevant chapter/segment and treat it as an alternative view — the primary source's terminology and ordering always win.
  4. Identify the **starting concept** (the first syllabus item not covered by any existing lesson) and the **stopping concept** (the furthest syllabus item reachable within the lesson's cell budget — default 40; the course document may set a different budget per lesson). These two concepts define the notebook's scope.
  5. Before naming the new notebook, scan `./lessons/` for existing filenames to prevent duplicate numbering.

  Completion criterion: The starting concept and the final stopping concept are stated, and the filename is unique in `./lessons/`.
- **Staged Epiphanies**: Scope 1–3 explicit AHA moments per notebook. An epiphany must feel like an unplanned surprise to the learner. To manufacture one:
  1. **Productive Failure (Dig Deep)**: Push the learner into a deliberate mathematical dead end that shatters their current intuition. A productive dead end is one where the learner's current tool provably fails for a reason that motivates the next tool.
  2. **Lateral Leap (Travel Sideways)**: Introduce an unexpected twist by importing a concept from `RESOURCES.md` or the course syllabus that has not yet been introduced in this notebook to re-frame the failure.
  3. **The Reveal**: Weave the exact resolution into the prose as a natural realization.
- **Explicit Code**: Use explicit for-loops, typed positional arguments, and shape comments.
- **Scratchpad Prose**: Write conversational, precise prose ("let us") that actively externalizes a stream-of-consciousness thought process.
- **Video Citations**: When lesson content draws on a video blueprint, cite it inline with a timestamped link (`[Lecture 1 @ 53:23](https://youtube.com/watch?v=<id>&t=3203)`). Prefer the lecture's own terminology, analogies, and worked examples over generic ones — `GLOSSARY.md` arbitrates when they conflict.
- **LaTeX Guardrails**: Render all LaTeX equations using raw strings (`mo.md(r"...")`) to prevent escape character drops. 
- **Plotting & Isolation**: Isolate figures with context suffixes strictly inside the cell (`fig_sim, ax_sim = plt.subplots()`). Return the raw `ax_sim` or `fig_sim` directly, keeping it completely unwrapped from `mo.ui` components. Color code consistently.
- **Hide Markdown Code**: Explicitly hide the code for all markdown cells (`mo.md(...)`) so the learner only sees rendered prose, keeping python logic cells fully visible as the System 2 scratchpad.
- **Global Imports**: Consolidate all heavy library imports (`mo`, `np`, `plt`, `torch`) exclusively into exactly one global top-level cell.
- **Crawl-Walk-Run**: Structure mechanics using this micro-cycle test-driven development:
  1. **Crawl (Theory)**: Math/physics in a hidden-code markdown cell.
  2. **Walk (Logic)**: Define pure Python logic functions in one cell. Invoke on a hardcoded test input in the next.
  3. **Run (Interactive)**: Define `mo.ui` sliders in one cell. Drive the pure functions with loops/datasets and output the interactive plot in the next.

## The Notebook Sequence (Default Budget: 40 Cells)

Choose a track: if the lesson's core output is a **proof, derivation, or identity verification**, use Foundations. If the core output is a **trained model, fitted curve, or data pipeline**, use Applied. When ambiguous, prefer Foundations — it's easier to extend a derivation into application than to backfill missing theory.
- **Applied Track**: For modeling and fitting. Features a naive attempt and manufactured failures.
- **Foundations Track**: For pure math, derivations, and verifying identities. Prove correctness by verifying strictly against analytical targets.

### Section Layout
Use this logical structure to shape the content, pacing, and pedagogy. Diverge only in Sections 1-4/5 based on the track. Apply the **Crawl-Walk-Run** micro-cycle to structure the internal cells of Sections that implement mechanics (marked below). Keep the framework invisible (don't use the labels "Section 1" or "Crawl-Walk-Run" in the output).

**Part N: [Title] - [Core Concept]**

**(Foundations Track only)**
- Section 1: The Question - [What Intuition Is Missing]
- Section 2: The Intuition - [Minimal Hand-Worked Example]
- Section 3: The Derivation - [First-Principles Result]
- Section 4: Implementation & Verification - [Raw Code vs. Hand-Derived Answer] (Invoke Crawl-Walk-Run)
- Section 5: The Stress Test - [Where It Strains] (optional)

**(Applied Track only)**
- Section 1: The Problem - [Mathematical/Physical Setup]
- Section 2: The Naive Approach - [Basic Implementation] (Invoke Crawl-Walk-Run)
- Section 3: The Diagnosis - [Why It Fails]
- Section 4: The Next Idea - [Hypothesis From Diagnosis] (Invoke Crawl-Walk-Run)

**(Both Tracks)**
- Section 5/6: The Abstraction (Read Evaluation Gate before proceeding)
- Section 6/7: The Exercise

### ⟳ Evaluation Gate (Post-Abstraction)
Stop and evaluate:
1. **The Wall**: If the notebook exceeds its cell budget unplanned, stop. Trigger the **Handoff Block**.
2. **Test-Driven Verification**: Execute the notebook top-to-bottom without errors via `uv run` from the workspace root. If an import fails because a dependency was never approved in Step 2, ask the user before `uv add`-ing it — then record the addition in the Step 5 report. If the `tdd` skill is available, use it for structured test scaffolding.
3. **Quality Check**: Pass the domain-specific **Diagnostic Checklist**. If the checklist fails due to a code error (wrong shapes, missing imports, numerical bugs), fix the code in place. If it fails due to a conceptual limitation (the approach itself cannot produce the expected result), label the cell as a dead end and loop back to Section 3. If The Wall is hit while looping, trigger the Handoff Block with the diagnostic evidence. If the next notebook also fails on the same issue, stop and ask the user.

### Diagnostic Checklist
**1. Math & Numerical Methods**: [ ] Analytical Match, [ ] Theoretical Convergence, [ ] Uniform Residuals
**2. Machine Learning & Optimization**: [ ] Monotonic Loss, [ ] Healthy Updates, [ ] Stable Gradients, [ ] Expressive Activations
**3. Physics-Informed Neural Networks**: [ ] Boundary Precision, [ ] Balanced Gradients, [ ] Conservation
**4. The Reactive Loop**: [ ] Direct Wiring, [ ] Cell Isolation

### The Handoff Block
When hitting **The Wall**, insert a final conclusion cell (replacing the Exercise section) to choreograph the transition. Write a cohesive narrative paragraph that weaves together the **Current State**, **The Wall** (why we must shift to a new notebook), the **Next Notebook Blueprint**, and the **Target File** (`XXXX-next-topic.py`). Next steps: The subsequent notebook recaps the handoff, hard-codes the best hyperparameters, and begins at Section 2 or 3.
