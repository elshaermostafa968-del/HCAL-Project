# Week 5: Flow and Architecture

**Academic Writing Coach · Transparency · 23 November 2026**
Runnable implementation, with local tests clearly separated from live-model evidence.

## Submission status

| Output | Included | Important limit |
|---|---|---|
| Conversation flow | Editable Mermaid, rendered diagram, implemented UI | Human route shows contacts; no actual transfer |
| System architecture | Editable Mermaid and rendered diagram; transparency marked | Lexical retrieval, not embeddings |
| Eight golden rules | Implementation checklist with test actions | No formal accessibility conformance claim |
| First backend-served live reply | Working provider clients and capture script | **Pending a real API key and successful model call** |
| Prompt log | Historical source notes and fill-in template | Team must recover exact historical prompts; no invented entries |
| Runnable demo | Full FastAPI + HTML/CSS/JS + 40 cases | Default local mode is not an LLM |
| Evaluation | 40 labelled fixture outputs, unit and browser smoke checks | Not held-out accuracy or human usability results |

## 1. Conversation flow

Greeting identifies AI, its scope, and the difference between a coach and an essay writer. Quick replies lead to paragraph checking, citation verification, help, or a person. The user picks a style and submits a fictional excerpt with one question.

Input is checked for length, context, and common requests for assignment generation. Weak or conflicting evidence produces uncertainty. A strong match selects one rule and its source. The local pipeline returns the case's fixed feedback; a configured live provider must return the same constrained JSON contract from the backend. The validator hides unsupported output rather than showing fabricated advice.

A feedback card includes the critique, rule type as text, hint level, source, evidence similarity, matched terms, and the retrieved rule ID. Follow-ups include previous/next hint, why, source only, editing the last message, another check, and closure. Two unhelpful ratings offer human support. Talk to a person is always available. Closure summarizes the rule and makes clear that the student's draft has not been rewritten.

See `flow.mmd` for the full editable flow and `flow.png` for its rendered form.

## 2. Architecture and the Transparency feature

1. **S1 safeguards:** 4,000-character maximum, scope heuristic, context question. API keys are only read server-side from environment or `.env`.
2. **S2 retriever [Transparency]:** style/category-filtered, IDF-weighted keyword similarity over the actual synthetic data. Similarity is shown as a score, not a probability of correctness. Weak or near-tied matches stop.
3. **S3 prompt builder:** includes only one selected rule/source and permitted JSON feedback. Student content is untrusted data, not instructions. No rewrites.
4. **S4 LLM client [Safeguard]:** 10-second HTTP timeout, one retry, then calm error plus human options. Gemini/OpenAI support, or explicit deterministic local mode.
5. **S5 validator [Transparency]:** exact response contract checks rule ID, label, feedback, and hint. An allowed rule ID alone is not enough to let invented text through.
6. **S6 composer [Transparency]:** actual dataset evidence feeds the source panel. A limitation note accompanies grounded feedback; errors and uncertainty are labelled.

`/feedback` stores choice/category-only JSONL, not drafts. `/health` reports mode and counts, never keys. See `architecture.mmd` and `architecture.png`.

## 3. Failure and recovery cases

| Situation | Result |
|---|---|
| Write my essay | Scope refusal and coaching options |
| Too little detail | One clarifying question |
| Citation style unspecified | Ask APA/MLA/IEEE before critique |
| Conflicting department/lecturer guidance | Uncertainty and ask instructor |
| Low or ambiguous match | No fabricated rule, show options |
| Unknown rule ID / changed model text / invalid JSON | Hide model answer, uncertainty |
| Missing key, API error, timeout | One retry then error, Try again, human contacts |
| Two unhelpful ratings | Offer human support, with reason choices |

Draft text stays in the open browser tab after a request failure. Reloading or Clear chat erases the tab's chat state. The server does not persist drafts. This is not an autosaved editor.

## 4. Backend response evidence

The included local evaluation was run on this implementation and is explicitly labelled local. It shows pipeline consistency only. The downloadable project includes no fabricated live response, fake screenshot, or invented test participant.

To complete the real-model requirement:

1. Follow the README to obtain your own key and choose a model available to your project.
2. Set the provider and key in `.env`, restart the backend, and open `/health`.
3. Run `python scripts/first_call.py` from the project root in a second terminal.
4. The script saves a JSON evidence file only for `status=ok` and `live_model_response=true`. Record the two terminals and show the browser source panel.

A real backend model call is made even though the validated teaching wording is deliberately extractive. Explain that trade-off honestly: this prototype proves a constrained model-backed workflow, not open-ended coaching intelligence.

## 5. Check-in readiness and remaining team work

- Open and run the app rather than describing it. Each member should explain S1–S6, the dataset, one fallback, and the evidence panel.
- Review original-source accuracy independently; structural advice is not automatically mandatory.
- Recover exact historical prompts, choose a project/dataset license, and add the team's actual changes to the prompt log.
- Run and capture a real-model response once a key exists.
- Conduct the five-person study and report actual objective results. Current objectives remain targets.
- Use only fictional examples. Do not publish real drafts, API keys, personal screenshots, or feedback logs.
