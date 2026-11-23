# Week 3: Users and Data

**Academic Writing Coach · Writing Assistant track · Transparency**
Updated implementation package, 23 November 2026. Fictional design profiles only.

## 1. Project and scope

The coach helps students understand grammar, academic structure, and APA/MLA/IEEE citation conventions through source-linked feedback. It supports conversational mentoring and rule-based verification without writing the student's assignment. The implemented prototype matches English fictional examples to 40 synthetic cases, returns one relevant rule and incremental hints, and stops when evidence is weak or local instructions conflict. It does not verify whether a publication exists.

## 2. Fictional personas

### Youssef Ibrahim: below-typical technical level

- Fictional Egyptian first-year computer-science student; Arabic is his first language. Technical level and cultural background are independent design attributes.
- Novice AI user. Comfortable with messaging but unfamiliar with prompt design, model limits, and verification.
- Accessibility need: visual fatigue and contrast sensitivity. Requires readable type, high contrast, keyboard controls, and explicit text labels, never color alone.
- Goal: understand basic citation and paragraph rules without losing his voice.
- Pain points: dense manuals, technical language, accepting an unexplained rewrite.
- Design response: one question at a time, plain-language hints, text badges, linked evidence, and a visible human route.

### Mariam Adel: typical technical level

- Fictional Egyptian second-year university student in a bilingual learning environment.
- Novice AI user for academic verification. She has tried chat interfaces but has little practice checking their evidence. This draft clarifies the original novice-to-moderate wording so there are at least two novice AI users overall.
- Goal: distinguish strict APA/IEEE formatting requirements from optional tone/structure advice.
- Pain points: unexplained flags, confusing styles, and edits that change her argument.
- Design response: choose a style before citation feedback; separate Mandatory rule from Style suggestion; show the rule and source; accept helpful/unhelpful feedback.

### Ziad Khaled: advanced technical level

- Fictional Nigerian third-year student in an international university setting. His name does not determine nationality or technical ability.
- Experienced AI user; evaluates output reliability and wants to inspect sources quickly.
- Goal: diagnose argument structure, inspect provenance, and avoid repetitive explanations.
- Pain points: generic praise, invented references, and overly simple repeated feedback.
- Design response: source-only shortcut, evidence panel, direct style links, hint-level control, and uncertainty disclosure.

## 3. Bias-check record

| Reviewed | Risk noticed | Change |
|---|---|---|
| Names/backgrounds | Mistaking culture for technical ability | Specify skills separately; no identity-based inference |
| AI experience | Original typical persona was novice-to-moderate | Make verification experience explicitly novice, preserving the two-novice requirement |
| Feedback labels | Treating passive voice or rhetorical preference as universally wrong | Use Style suggestion and explain exceptions |
| Visual status | Color-only labels exclude some readers | Text labels, readable contrast, focus states, semantic landmarks |
| Data/examples | Accidentally presenting fictional publications as real | All snippets are labelled synthetic; no source-existence claims |
| Language | English keyword matching may not serve Arabic queries equally | Declare English-first scope and require multilingual evaluation before expansion |

These are design-review findings, not measured usability results.

## 4. Data source description

The implemented file `academic_guidelines_dataset.json` contains exactly **40 synthetic teaching cases**: Grammar & Syntax 10; Citation & Formatting 12; Structural & Argumentative 12; Insufficient Context 6. No case contains real student writing or personal screenshots. Names and bibliographic examples are fictional. Each case includes a short draft, an issue description, a rule paraphrase, an official or university source link, uncertainty guidance, three progressive hints, reference feedback, and expected validation behavior.

The dataset fits the writing-assistant track because students must learn why a rule applies and revise their own work. APA, MLA, and IEEE links support citation-specific conventions. Harvard College Writing Center and Purdue OWL links support general writing guidance. These are public sources, not a claim that the manuals are openly licensed. Rules are summarized in original wording, and guide content remains third-party property. The team must record its own licensing decision before making a redistribution-license claim. See `data-and-permissions.md` for the permission caveat.

The required schema field `verified_reference_feedback` is retained, but each value states its actual status: source-linked editorial paraphrase requiring independent team review, not external expert certification. All source URLs are supplied for audit. A lexical retriever exposes similarity and stops rather than guessing when the match is weak. Dataset fixture checks do not prove correctness on unseen student writing.

## 5. Ten-field schema

1. `case_id`: stable identifier, GS/CF/SA/IC prefix.
2. `category`: one of the four categories.
3. `student_draft_snippet`: fictional text.
4. `observed_issue`: searchable issue description.
5. `expected_rule`: text and mandatory/suggestion label.
6. `style_manual_reference`: title, URL, style, provenance, review date.
7. `uncertainty_fallback_notes`: limits or clarification guidance.
8. `progressive_hints`: three levels, never a replacement draft.
9. `verified_reference_feedback`: feedback text and review caveat.
10. `validation_tests`: input, expected status/rule, forbidden effects.

## 6. Prompt log: source integrity

The original Week 3 PDF contains one recorded ChatGPT prompt for the interaction flow, but does not include the exact Gemini prompt. Do not reconstruct it as if it were historical evidence. Preserve the original report separately, and recover the actual prompt from the team's own history if available.

| Entry | Tool | Exact prompt available? | Output / team review |
|---|---|---|---|
| A1, original Week 3 | ChatGPT | Yes, in original course PDF | Flow proposal; team reports adding uncertainty fallback |
| A2, original Week 3 | Google Gemini | No, pending team recovery | Rule-matching proposal reported; exact output also needs original evidence |
| New implementation review | Team to record its actual chat tool and prompt | Pending | Review generated dataset, test outputs, accessibility, and source accuracy; record edits honestly |

For future entries use `prompt-log-template.csv`. Do not submit blank fields as completed work. A source PDF's assertion that a log is complete does not supply a missing prompt.

## 7. Live check-in checklist

- Open this report and the 40-case JSON, not just a description.
- Explain one case from each category and why uncertainty is required.
- Demonstrate both novice needs and advanced shortcuts.
- Explain why a style suggestion is not a mandatory formatting rule.
- Confirm source permissions and recover missing historical prompt evidence.
- Every member should be able to explain any output.
