# Academic Writing Coach

A runnable university teaching prototype for the **Transparency** HAI principle. HTML/CSS/JavaScript frontend, Python FastAPI backend, and 40 fictional guideline cases. It gives coaching and step-by-step hints, never essay generation. For the three-stage onboarding, recording script and submission checklist, see `README-W6-7.md`.

## Quick start (clean clone)

Requires Python 3.10 or newer and Git.

```sh
git clone https://github.com/elshaermostafa968-del/HCAL-Project.git
cd HCAL-Project/milestones/week-06-07/chatbot
python -m venv .venv
```

Activate the virtual environment (pick the line for your shell):

```sh
# Windows cmd
.venv\Scripts\activate.bat
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

Install and run (the same on every system, from the `chatbot` folder, not `backend/`):

```sh
python -m pip install -r requirements.txt
python -m uvicorn backend.app.main:app
```

Open **http://127.0.0.1:8000**. Do not open `frontend/index.html` directly. Add `--reload` to the last command only while editing code. `/docs` has the API documentation and `/health` shows the active provider.

Check that it started: `http://127.0.0.1:8000/health` should show `"provider":"local"`, `"live_model":false` and `"dataset_cases":40`. Every reply card says **Local demo, No live model**.

## Choose a provider

Set the provider in a local `.env` file in the `chatbot` folder (the same folder as `requirements.txt`). Restart uvicorn after changing it.

| Provider | `.env` setting | Key needed |
|---|---|---|
| Local demo (default) | `LLM_PROVIDER=local`, or no `.env` at all | None |
| Gemini | `LLM_PROVIDER=gemini` | `GEMINI_API_KEY` |
| OpenAI | `LLM_PROVIDER=openai` | `OPENAI_API_KEY` |

Local mode returns fixed, source-linked feedback from the retrieved case and calls no external service.

To use Gemini, copy the template and fill in your own values:

```sh
# Windows cmd
copy .env.example .env
# Windows PowerShell, macOS, Linux
cp .env.example .env
```

```ini
LLM_PROVIDER=gemini
GEMINI_API_KEY=<your own key goes here, never in the repo>
GEMINI_MODEL=<model name>
```

- `GEMINI_API_KEY` is the required variable. Create it in your own Google AI Studio account (https://ai.google.dev/gemini-api/docs/api-key). Never paste it into chat or code.
- `.env` is listed in `.gitignore` and stays on your machine. Do not upload or commit it. The tracked `.env.example` has empty values.
- `GEMINI_MODEL` is optional. The code default is `gemini-2.5-flash`. The team reported using `gemini-3.1-flash-lite` for its live call. That is the team's report. It is not shown by any response in this repository and Google's availability for it was not checked here. Confirm that the model is available to your own project and quota. Pricing and free-tier limits are on Google's pages: https://ai.google.dev/gemini-api/docs/pricing and https://ai.google.dev/gemini-api/docs/rate-limits
- Variables already set in your terminal win over `.env`. In Windows cmd, `set LLM_PROVIDER=` clears one for the current window. In PowerShell use `Remove-Item Env:LLM_PROVIDER`, and in macOS/Linux use `unset LLM_PROVIDER`.
- With Gemini or OpenAI selected, a missing or invalid key gives an error reply. It never switches silently to local mode. Reply cards say **Live model** only when the provider answered.
- Use synthetic text only. Some free tiers may use inputs to improve products, so read the provider's current terms first.

## What this tool does not do

- It does not write or rewrite your assignment, and it does not grade your work.
- It does not check that a source exists or that a quotation is accurate.
- It is not a general grammar engine, an academic-integrity detector or a production service. It covers 40 fictional teaching cases and can miss legitimate requests.

## Status and verification

- **Independent local run:** a fresh clone of this repository, installed from `requirements.txt` on Linux (Python 3.10) in local mode with no key, started with the command above. `/health` showed provider `local` and 40 cases, and a sample question returned a normal reply. Windows and macOS were not tested here. `pytest` (10 of 10) and `eval/run_eval.py` (40 of 40) pass in local mode. These evaluation cases reuse the project's own fixtures, so this is a smoke check, not accuracy, held-out testing, latency or usability evidence.
- **Live Gemini:** a teammate reported one successful live call on 2026-11-26. We have not independently verified it and have not re-run live Gemini. Treat live mode as unverified. `python scripts/first_call.py` (while the server is running with a real provider) saves `evidence/live-*.json` only after a successful live response.
- **Screenshot:** `docs/live-gemini-reply.jpg` shows live Gemini mode on the current build, one captured reply. The 40-case suite remains local smoke consistency, not live evidence.

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

