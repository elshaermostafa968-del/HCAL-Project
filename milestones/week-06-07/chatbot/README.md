# Academic Writing Coach

**Weeks 6-7 update:** start with `README-W6-7.md` for the three-stage onboarding, recording script, new unsafe path, and exact submission checklist. This README retains the original provider/setup documentation.

A runnable university teaching prototype for the **Transparency** HAI principle. HTML/CSS/JavaScript frontend, Python FastAPI backend, and 40 fictional guideline cases. Coaching and incremental hints, never essay generation.

## Start locally

Python 3.10 or newer. Run all commands from this project folder, not `backend/`.

```sh
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload
```

Open **http://127.0.0.1:8000**. Once installed, the last command is the one-command launch. No Node build, database, API key, or external service is needed for the default local demo. `/docs` has the interactive API documentation; `/health` reports the active provider. Do not open `frontend/index.html` directly.

## Local demo versus real-model evidence

Default `LLM_PROVIDER=local` returns deterministic, source-linked feedback from the retrieved case. Every card explicitly says **LOCAL DEMO / NO LIVE MODEL**. This proves the frontend/backend pipeline works. **It does not meet the check-in's first real model response requirement.** No successful live call has been claimed or included.

For a real model, create `.env` in the project root by copying `.env.example`:

```ini
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_own_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Or choose `LLM_PROVIDER=openai`, `OPENAI_API_KEY`, and `OPENAI_MODEL`. Restart uvicorn after changing `.env`. Existing environment variables take priority over `.env`. Real-provider mode does not silently switch to local when a key is missing or invalid.

### Obtain a Gemini key

1. Follow Google's official key guide: https://ai.google.dev/gemini-api/docs/api-key?authuser=9
2. Open the AI Studio API-key page linked there, sign into your own account, select/create your project, and create the key.
3. Store it only in the local `.env`. Never send it in chat, commit it, or put it in JavaScript.
4. Confirm the model is available to your project and check its free-tier quota. Some models have free usage, but access, regions, quotas, and pricing can change. Creating a key does not guarantee free unlimited calls. Do not enable billing unless your team intends to pay.

Official pricing: https://ai.google.dev/gemini-api/docs/pricing?authuser=002
Official quotas: https://ai.google.dev/gemini-api/docs/rate-limits?authuser=0
REST API contract: https://ai.google.dev/api/generate-content?authuser=2

Use synthetic text only. On some free tiers, provider inputs can be used to improve products. Read the provider's current terms before enabling live mode.

### Capture the first backend-served real response

Keep the server running in terminal 1; in terminal 2, with the same virtual environment:

```sh
python scripts/first_call.py
```

The script refuses local-mode evidence and saves a timestamped `evidence/live-*.json` only after a successful response with `live_model_response=true`. Record both terminals and the browser's source panel. If the model cannot be reached, no live evidence is saved. Keep using local mode to demonstrate other paths while resolving the live call.

## Three-minute check-in demo

1. Start the backend and show `/health`: 40 cases, correct category counts, explicit provider.
2. Choose APA and submit: `Check APA missing year: Earlier research supports this claim (Nadir).`
3. Show the **Mandatory rule** text badge, original rule/source, evidence similarity, and **Why this rule?** panel. The year is not invented.
4. Choose General and submit: `passive voice overuse: The experiment was planned by the team. The results were checked by the team.` Show **Style suggestion**. Passive voice is not forbidden.
5. Use **Next hint**, **Previous hint**, **Edit last message**, and **Show source only**. Revise the sample yourself.
6. Try `Please write my essay about transport.` (scope refusal), `help` (one context question), and `Quantum jellyfish dance through invisible marshmallow galaxies.` (uncertainty).
7. Rate two separate replies unhelpful to show human handover. Or use the always-visible button. This shows contact options, not a real transfer or booking.
8. Choose **I'm done**, review the closure summary, then **Clear chat**.
9. With a real provider/key configured, run `scripts/first_call.py` for the actual model requirement.

## Architecture and safeguards

```text
Browser -> POST /chat -> S1 input checks -> S2 lexical retrieval [Transparency]
        -> S3 constrained JSON prompt -> S4 backend model call (or labelled local mode)
        -> S5 strict output validator [Transparency]
        -> S6 evidence + rule label + hint + uncertainty -> Browser
Browser -> POST /feedback -> choice/reason-only local JSONL
```

- **S1:** 4,000-character limit, common English/Arabic essay-generation refusals, short-input context question. Heuristic filters are not complete intent detection.
- **S2:** IDF-weighted keyword cosine similarity over case snippets and issue descriptions; style/category filters; low/ambiguous matches stop. Not embeddings and not a correctness probability. Exact fictional fixture matches are intentionally easy to demonstrate.
- **S3:** Student text is data. Prompt restricts the model to a single retrieved rule, JSON, a textual rule label, and no rewrites.
- **S4:** Gemini/OpenAI keys stay server-side. 10-second HTTP timeout, one retry (two attempts maximum), then a calm error and human contact options. Invalid key and timeout do not masquerade as success.
- **S5:** Unknown rule IDs and *any* text not matching the retrieved case's allowed feedback/hint are rejected. This is a deliberately extractive prototype: even live-mode wording is fixed, not free-form conversation. This trades flexibility for auditable grounding and prevents a valid rule ID being attached to invented content.
- **S6:** Evidence is composed from the actual retrieved case, not generated after the answer. Hints escalate from 1 to 3 without rewriting the draft.
- **Uncertainty:** Unknown citation style, insufficient context, conflicts, low matches, and invalid model output do not get a confident diagnosis. One match is not a full-draft review.

See `docs/flow.mmd`, `docs/architecture.mmd`, `docs/golden-rules.md`, and `docs/evaluation-plan.md`.

## API

`POST /chat`

```json
{"message":"Check APA missing year: Earlier research supports this claim (Nadir).","style":"APA","category":"Auto","hint_level":1}
```

`status` is `ok`, `needs_context`, `out_of_scope`, `uncertain`, `handover`, `unsafe`, or `error`. Responses include `mode`, `live_model_response`, `latency_ms`, an opaque `response_id`, and, when grounded, evidence with a real rule ID and source URL. Invalid payloads return HTTP 422. Model-service failures are safe JSON workflow results, not raw provider exceptions.

`POST /feedback`: `response_id`, anonymous random browser-tab `session_id` (UUID), `helpful` (boolean), and a reason category (`clear`, `unclear`, `wrong_rule`, `not_relevant`, `too_complex`, `other`). Feedback writes no drafts, IPs, provider output, keys, or browser session identifiers. The session identifier is used in bounded volatile memory only. Feedback logs are local under `data/feedback.jsonl` and git-ignored. Delete this file to reset saved ratings. Recent response IDs expire on restart or after 2,000 responses.

`GET /health`: connectivity, mode, configuration status, dataset counts. Never returns keys.

## Tests and evaluation

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
python eval/run_eval.py
# Optional visual regression / browser smoke checks:
python -m playwright install chromium
python tests/browser_smoke.py
```

The 40-case harness saves `eval/results/metrics.json` and full outputs. It uses labelled fixtures also present in the dataset, so it is a smoke check, **not held-out model accuracy**. Model error/retry, invalid JSON/rule/content, scope, context, schema, and feedback paths are tested separately. The browser test starts and stops its own temporary local server.

O1 rule accuracy ≥90%, O2 independent revision ≥80%, O3 label comprehension ≥90%, O4 average total UI latency <2s, and O5 uncertainty handling ≥95% are **targets, not achieved human-test results**. Local backend timings do not prove live API or end-to-end UI latency. Retry/error paths can take longer than the latency target. Conduct the five-person usability study and source audit before claiming these objectives.

## Dataset and limits

`academic_guidelines_dataset.json` has exactly ten top-level fields per record and the requested 10/12/12/6 split. All names, snippets, and bibliographic examples are fictional. Source-linked rules are editorial paraphrases of public APA/MLA/IEEE and university writing-center guidance, not copied manuals. Structural advice is labelled suggestion, not an APA mandate. `verified_reference_feedback` retains the requested schema name but includes a clear verification caveat: no external expert certification is claimed.

This is a small English-language prototype, not a general grammar engine, publication lookup tool, academic-integrity detector, production service, or real institutional handover system. Unsupported requests may not match even when legitimate. Citation formatting feedback does not prove a work exists. No university contact details were supplied, so contact routes are generic and explicitly ask students to use their own syllabus/university site.

Default binding is localhost. Do not expose this version to the public internet: it lacks authentication, distributed rate limiting, durable per-user state, production retention controls, HTTPS deployment, and comprehensive abuse protection. Do not upload real student data. `docs/data-and-permissions.md` describes third-party source restrictions and a proposed license that the team must adopt before claiming permission to redistribute.
