# 1. Team card (team name, members, project, HAI principle)

Team name: Academic Writing Coach. Members: MEMBERS_PENDING. Project: Academic Writing Coach. Track: Writing Assistant / Academic Writing Support. HAI principle: Transparency. Milestone: Weeks 6 and 7, Milestone 3.

This design pack describes a working English-first teaching prototype. The system explains one source-linked rule and offers hints; students revise their own fictional text. The default mode is deterministic local feedback, clearly labelled as not a live model. Gemini/OpenAI mode is available through the team's own backend, but no successful live API response is claimed without actual capture evidence.

Submission status: documents, code, and synthetic tests are prepared; the team records its own 3–5 minute video, recovers any missing historical prompts, confirms its membership/licensing information, and ensures each member commits from their own account. No assistant-authored commit can satisfy a member's own-account requirement.

# 2. Personas (revised)

## Youssef Ibrahim: below-typical technical level

Fictional Egyptian first-year computer-science student; Arabic is his first language. He is a novice AI user who uses messaging apps but has little experience judging model evidence. His visual fatigue and contrast sensitivity create an accessibility need for readable type, high contrast, visible focus, text labels, and low-density guidance.

His goal is to learn basic citation and paragraph rules while keeping his own voice. Dense manuals, unfamiliar terms, and unexplained automatic rewrites are pain points. The revised onboarding gives him a worked example first, then a guided citation task, then independent work with help always available. He can repeat or skip stages and is never scored by an inferred ability level.

## Mariam Adel: typical technical level

Fictional Egyptian second-year university student in a bilingual setting. She is a novice in AI-assisted academic verification, even though she knows common digital tools. She wants to distinguish APA/MLA/IEEE requirements from optional writing advice.

Opaque flags and unwanted changes to her argument are pain points. The revised co-pilot stage asks her to choose the style and inspect a Mandatory rule label, source, and hint. Independent mode keeps these controls available without forcing repeated explanations. Her novice classification clarifies the earlier novice-to-moderate draft and ensures two novice AI users across the personas.

## Ziad Khaled: advanced technical level

Fictional Nigerian third-year student in an international university setting. He is an experienced AI evaluator and advanced technical user. His background and name do not determine his skills; those attributes are specified independently.

He wants concise structural feedback, direct source access, and visible evidence limits. Generic praise and fabricated references are pain points. He can inspect the demonstration, skip directly to independent mode, request source-only output, and challenge an unsupported match through feedback or a person. He is not forced to complete a beginner tutorial.

## Revision and bias checks

All profiles, snippets, and example publications are fictional. No identity is used to score writing or predict technical ability. Mandatory rules are separated from stylistic advice, passive voice is not automatically an error, and unknown local requirements go to an instructor. English-only retrieval and the lack of an assistive-technology user study remain limitations, not hidden claims of inclusion.

# 3. Journey maps (revised)

## Youssef's journey

| Stage | Student action and pain point | Revised support and principle |
|---|---|---|
| Start | Unsure what an AI writing coach does | AI scope and local/live disclosure appear before input; worked example makes the boundary concrete |
| Ask | Does not know how to phrase a useful question | Co-pilot loads one fictional APA example and tells him what to inspect |
| Understand | Dense terms and color-only flags cause difficulty | Readable text, text badges, one hint at a time, source link and evidence explanation |
| Act or recover | Revises independently or remains unsure | Previous/next hints, edit/resend, context question, help and human options |
| Finish | Needs a clear next step | Summary of the rule, helpful/unhelpful rating, clear chat; no draft rewrite |

## Mariam's journey

| Stage | Student action and pain point | Revised support and principle |
|---|---|---|
| Start | Wants citation feedback without confusing styles | Greeting explains limits; style selection remains visible |
| Ask | Chooses APA and submits fictional citation | Co-pilot guides the first task; rule matching uses the chosen style |
| Understand | Needs to tell requirements from preferences | Mandatory rule / Style suggestion words, Why this rule?, direct official source |
| Act or recover | Makes her own edit and requests another hint | No automatic rewrite; source stays attached; feedback asks a reason |
| Finish | Wants to know if the task is complete | Explicit closure and independent-mode transition; two unhelpful ratings offer a person |

## Ziad's journey

| Stage | Student action and pain point | Revised support and principle |
|---|---|---|
| Start | Wants to bypass basic explanations | Skip to independent mode is explicit and reversible |
| Ask | Asks a narrow argument or citation question | Style/focus controls and one relevant retrieved rule |
| Understand | Distrusts ungrounded model claims | Actual rule ID, source, matched terms, similarity caveat and strict output validation |
| Act or recover | Challenges a weak or conflicting answer | Uncertainty rather than fabricated certainty; source-only shortcut and human route |
| Finish | Wants concise takeaway | Rule-based summary, feedback, clear/new check; no proficiency claims |

# 4. Onboarding storyboard

## Stage 1: The system does it

Screen title: "1 of 3 · The system does it". The first message identifies an AI writing coach, explains grammar/structure/citation support, and says it never writes the essay. A local/live mode banner and synthetic-data warning appear before a student task. **This is where Transparency first appears**, at Inform level; the worked source panel then introduces Explain level.

The user selects "Show a worked example". The actual interface sends a fictional APA example through `POST /chat`, not a hard-coded fake answer card. The case is: "Check APA missing year: Earlier research supports this claim (Nadir)." The backend returns rule CF-001, its official source, a Mandatory rule label, hint 1, and an explicit evidence-score limitation. When it succeeds, "Continue to co-pilot" becomes available. If the provider fails, the system shows recovery instead of pretending the stage succeeded.

## Stage 2: Co-pilot

Screen title: "2 of 3 · Co-pilot". "Load guided task" fills the same synthetic citation so the learner can compare the rule without handling private data. The guidance asks the learner to choose APA, send the task, open "Why this rule?", try a hint, and revise independently. The tool does not invent a year or certify the user's revision.

A successful guided check changes the action to "Continue independently". Completion means the backend check ran, not that the learner passed a skill test. The user decides when to move on, may ask for help, and may skip the stage. Source and hint controls remain in the chat history.

## Stage 3: The user does it

Screen title: "3 of 3 · The user does it". The composer is cleared so the learner can enter a new fictional excerpt independently. Help, previous/next hint, source-only access, uncertainty, feedback, and the persistent "Talk to a person" button remain available on request.

The user can restart guided onboarding or clear the session. This returns control to the learner without implying that hidden tracking, saved proficiency, or an institutional handover has occurred. Chat state lasts only in the browser tab; refreshing can erase it.

## Persona routes through all three stages

| Persona | System demonstration | Co-pilot | Independent work |
|---|---|---|---|
| Youssef | Reads plain scope/mode label and watches one source-linked example | Uses the loaded task, keyboard controls, and one hint; can repeat | Enters a new fictional excerpt with Help visible; contacts a person if stuck |
| Mariam | Notices citation source and Mandatory rule text | Chooses APA and compares a rule to her own revision | Chooses style for later tasks; uses optional explanations and feedback |
| Ziad | Inspects rule ID/source/score caveat quickly | May try the guided task or skip it; never locked out | Source-only shortcut, narrow questions, uncertainty inspection, direct control |

Storyboard descriptions accompany the working-screen captures in the final PDF. The images are examples of the actual local implementation, not substitutes for this text or for the required video.

# 5. Feature Choice Board

| Feature | What it does | Personas served | HAI Ladder level | Core or optional for the user |
|---|---|---|---|---|
| Scope and mode disclosure | Identifies AI scope, no essay generation, local/live mode and synthetic-text boundary | All, especially Youssef | Inform | Core: always shown |
| Three-stage onboarding | Demonstration, guided attempt, independent mode with repeat/skip controls | All; Ziad may skip | Inform / Allow control | Optional pathway; stages remain available |
| Style and focus selection | Lets student choose APA/MLA/IEEE or general writing and a concern | Mariam, Ziad | Allow control | Core for citation-specific judgment; focus filter optional |
| Source-linked rule card | Attaches Mandatory rule or Style suggestion in words to grounded feedback | All | Explain | Core: attached to supported feedback |
| Why this rule? / source only | Reveals actual source, rule ID, similarity and score caveat; concise source shortcut | Ziad, Mariam | Explain | Optional expansion; source identity is still core |
| Progressive hints and reversal | Offers hints 1–3, previous hint, edit/resend without replacing student prose | Youssef, Mariam | Allow control | Optional, student chooses |
| Uncertainty and recovery | Stops on missing context, weak/conflicting evidence or invalid model content; retry after API error | All | Inform / Allow control | Core when needed; never hidden by user settings |
| Helpful/unhelpful feedback | Records choice and reason category, offers a person after two distinct unhelpful responses | Mariam, Youssef | Enable feedback | Optional rating; human control always available |
| Human route and closure | Shows instructor/writing center/librarian/official sources; summarizes and clears on request | All | Allow control / Enable feedback | Optional action, always reachable; no automatic message or booking |

Nine features are listed. "Core" means a necessary safety/transparency element or task prerequisite, not compulsory tutorial completion. Optional controls never switch off source attribution, uncertainty, or input safeguards.

# 6. Accessibility plan

## Documents

Use real text, actual heading styles, readable fonts, left-aligned body text, generous spacing, and tables with repeated header rows. The PDF is generated from text, not screenshots of slides. Keep diagrams supplemental: include a title, meaningful alt text in the editable Word version, and a 2–4 sentence plain-text description immediately below each screenshot or storyboard image. Provide the same screen flow in written form so no essential information depends on seeing an image.

Use dark text on a light background and check contrast with a tool rather than judging by color names. Avoid color-only labels, tiny captions, dense slide layouts, and wide unbroken tables. The PDF should be checked for text extraction, reading order, and heading/navigation support; generation alone is not a PDF/UA or tagged-PDF conformance claim. The editable text and table content remain available for revision.

## Chat interface

- All actions use native buttons, inputs, selects, links, details, and dialog controls. Tab reaches them; Enter sends and Shift+Enter inserts a new line. An explicit Send button is available.
- Labels identify the style, focus, and fictional-text input. Chat uses `role=log`, polite live updates, speaker labels, and a separate busy status. Test whether announcements are useful and not repetitive.
- Text status includes Mandatory rule, Style suggestion, Local demo, uncertainty, and error wording. Green/amber decoration is never the only signal.
- Visible focus outlines, minimum 44px button heights, readable relative body text, wrapping, mobile reflow, browser zoom, and reduced-motion preference support comfort and control.
- The human button stays in a sticky header. A native dialog provides focus containment and Escape dismissal; verify focus returns to the opener. Links to external guides have descriptive names.
- Onboarding is skippable and repeatable. No time limit or forced proficiency gate. Independent mode keeps help available without erasing the learner's choice.

## Persona-specific need

Youssef's contrast sensitivity and visual fatigue are addressed with high-contrast foreground/background colors, no color-only meaning, larger chat text, short paragraphs, one hint at a time, and keyboard operation. This is a design response, not a diagnosis or proof that the interface works for every person with similar needs. Ask consenting participants about legibility and effort without collecting medical details.

## Testing and evidence plan

| Check | Method and success criterion | Status |
|---|---|---|
| Keyboard | Complete all three stages, send, inspect evidence, rate, open/close human dialog and clear with keyboard only; no trap | Browser smoke checks plus manual keyboard review; assistive-tech session still needed |
| Screen reader | NVDA/Firefox or VoiceOver/Safari: headings, labels, mode, busy state, new reply and dialog announced in logical order | Planned with actual assistive technology; not claimed complete |
| Zoom/reflow | 200% zoom and narrow phone widths; no lost controls, clipped core text or page-level horizontal overflow | Automated narrow-width check; additional manual zoom review |
| Contrast | Compute text/background contrast; target at least 4.5:1 normal text and 3:1 large text; inspect focus visibility | Programmatic palette check plus visual review |
| Meaning without color | Read every status and rule label in grayscale | Text labels implemented; visual check |
| Documents | Extract PDF text, inspect every page for clipping, check headings and alt text in Word, read table order | Text/layout checks before handoff; formal accessibility audit not claimed |
| Persona usability | At least five peers use fictional tasks; include novice and keyboard tasks, label-comprehension questions, independent revision, and comfort notes | Not yet conducted; do not invent success rates or SUS |

The 40-row spreadsheet includes normal, edge-case, out-of-scope, and unsafe prompts from each persona's viewpoint. It is a labelled test set, not proof that every expected behavior succeeds. Actual local observations are saved separately, and failures or weak context matching should remain visible for review. The team's O1–O5 thresholds remain targets until independently measured.
