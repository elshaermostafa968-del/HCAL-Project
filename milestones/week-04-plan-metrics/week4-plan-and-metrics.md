# Week 4: Project Plan v1

**Academic Writing Coach · Milestone 2 · Transparency**
Updated plan aligned with the runnable Week 5 prototype, 23 November 2026.

## 1. Persona journey maps

### Youssef: below-typical, novice AI, contrast sensitivity

| Stage | Action / pain point | Transparency and support |
|---|---|---|
| Start | Opens tool, anxious about a dense style manual | AI scope and local/live label explain what the tool can do |
| Ask | Shares a fictional paragraph; does not know prompt language | Plain quick replies and one context question reduce jargon |
| Understand | Finds formal terminology difficult | Short hint, textual rule label, readable contrast, source link |
| Act or recover | Tries an independent revision; may still be stuck | Previous/next hint, edit/resend, persistent human route |
| Finish | Wants to remember what to change | Closure summary and Clear chat; draft never rewritten |

### Mariam: typical technical level, novice academic AI verifier

| Stage | Action / pain point | Transparency and support |
|---|---|---|
| Start | Unsure whether a citation follows APA or IEEE | Clear style selector before style-specific judgment |
| Ask | Pastes a fictional citation and identifies concern | Scope/context checks avoid arbitrary formatting advice |
| Understand | Wants to know why a correction is needed | Mandatory rule versus Style suggestion; actual rule/source attached |
| Act or recover | Revises the citation and checks consistency | Evidence panel and hint progression support her own work |
| Finish | Rates whether the advice was understandable | Helpful/unhelpful controls; reason categories; summary |

### Ziad: advanced technical level, experienced AI evaluator

| Stage | Action / pain point | Transparency and support |
|---|---|---|
| Start | Wants evidence quickly, not a long tutorial | Quick replies and source-only shortcut |
| Ask | Asks about a narrow argument issue | One retrieved rule with a visible similarity score |
| Understand | Doubts generic claims and fabricated references | Source panel shows rule ID, matched terms, actual source, and score limits |
| Act or recover | Challenges weak evidence or local conflicts | Uncertainty and official guide/instructor options, not invented rules |
| Finish | Needs concise next steps | Summary, feedback, and a fresh check without hidden rewriting |

## 2. Measurable objectives

| ID | Objective type | Target | Measurement |
|---|---|---|---|
| O1 | AI quality / source accuracy | ≥90% | Independent source audit and held-out rule checks, supported claims / all assessed claims |
| O2 | User experience / task success | ≥80% | Five or more peers independently revise fictional tasks against a rubric |
| O3 | Principle: transparency comprehension | ≥90% | Correct classifications of mandatory rules vs suggestions, plus source understanding questions |
| O4 | Performance | Mean end-to-end UI latency <2s | Browser submit-to-render timings, separate local/live and retry/error groups |
| O5 | Principle: uncertainty | ≥95% | Held-out ambiguous/conflicting/unverifiable cases correctly avoid unsupported certainty |

These are targets, not achieved results. The prototype's local fixture tests cannot establish human revision success, SUS, or live-provider performance. Ten-second timeout plus one retry can exceed the normal latency target; report that path separately, never hide it in a fast-path average.

## 3. HAI Principle Ladder

| Level | Interface and backend implementation | Linked objective |
|---|---|---|
| Inform | AI identity, scope/no essay-writing, synthetic text warning, explicit local/live status | O2 |
| Explain | Retriever rule/source/similarity, evidence panel, source-only shortcut, output validation | O1 |
| Allow control | Style/focus/hint choices; uncertainty; no draft rewrite; human route | O5 |
| Enable feedback | Helpful/unhelpful plus reason; human option after two unhelpful ratings | O3 |

O4 supports the experience across all levels. Similarity is not model confidence; the interface says so explicitly.

## 4. Tool choices and grounding

- **Interface:** semantic HTML5, CSS3, vanilla JavaScript. No frontend build step.
- **Backend:** Python FastAPI, `/chat`, `/feedback`, `/health`, local static hosting on the same origin.
- **Knowledge source:** 40-case synthetic JSON, linked to public APA/MLA/IEEE and university guidance. This is not a full grammar or citation-verification corpus.
- **Retriever:** transparent IDF-weighted lexical similarity with thresholds, style filter, and ambiguity stop.
- **Model:** hosted Gemini or OpenAI selected through `.env`. Deterministic local mode makes the no-key demo runnable but is not real-model evidence.
- **Grounding:** strict extractive contract. The model may return only the selected case's rule ID, exact reference feedback, exact hint, and label. Anything else is hidden as uncertainty. This is narrower than general conversational generation and is intentional.
- **Storage:** no drafts persisted; category-only anonymous feedback in a git-ignored JSONL file. Real-provider mode sends synthetic excerpts to that provider.
- **Version control:** organize weeks in separate folders. Preserve real Git history. Do not fabricate weekly commits or teamwork that has not occurred.

## 5. Evaluation plan

Automated checks cover dataset counts/schema, fixture retrieval, scope/context/uncertainty, missing-key error, one retry, unsupported model output, and feedback handling. A 40-case harness writes JSON outputs and metrics. Because these prompts reuse dataset fixtures, report the number as implementation consistency only.

Conduct at least five consenting peer sessions with fictional tasks. Include one keyboard-only task, novice-friendly instructions, label-comprehension questions, and a human-route task. Record random IDs instead of names. Use the standard SUS questionnaire after testing; do not invent results or replace it with the app's thumbs rating. A blank observation table is in `evaluation-plan.md`.

## 6. Prompt log and submission gates

The provided Week 4 PDF does not contain exact weekly prompts. Recover originals where available, then add exact prompt, actual tool, output, edits, and rationale to `prompt-log-template.csv`. Mark missing history as missing rather than inventing it.

Before submission: open this plan, run the Week 5 demo, explain every objective's denominator, show the principle inside the pipeline, and distinguish targets from measurements. Every team member must be able to explain any output.
