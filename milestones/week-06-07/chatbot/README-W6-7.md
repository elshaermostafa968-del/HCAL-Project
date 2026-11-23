# Weeks 6 and 7: record this version

This is the revised chatbot for Academic Writing Coach's Milestone 3. It preserves the working Week 5 backend and adds a real three-stage onboarding: a backend-served example, a guided attempt, and independent mode with optional help. Skip and restart are always under the student's control. The guided check does not certify learning or score the student.

## Run locally

Python 3.10+; open a terminal in this `chatbot` folder:

```sh
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload
```

Open http://127.0.0.1:8000. Do not open the HTML file directly. The full provider configuration and limits are in README.md. Local mode is labelled and needs no key. A successful live response still requires your own configured provider/key; run `python scripts/first_call.py` to capture real evidence. Do not show `.env`, keys, real student writing, account details or personal notifications in the recording.

## What changed

- Working onboarding panel: Show a worked example -> Continue to co-pilot -> Load guided task -> submit -> Continue independently.
- Skip to independent mode, restart guidance, persistent help and human route.
- Larger chat text, minimum 44px button heights, mode/status words, and mobile reflow.
- An `unsafe` workflow result for requests to fabricate sources/results, conceal plagiarism, or share secrets/personal records. This heuristic is not a complete moderation system.
- Ten unit-test groups and a separate three-stage browser smoke test; no real-person usability outcomes claimed.

## Record the 3:50 demo

Follow the submitted one-page Demo Script. Record your own running app, with voice-over or captions, in the specified order. Keep the style selector on APA for the main fictional task. Inspect Why this rule? and its source/score limitation. Show the essay-generation refusal and recovery. Never edit a failed API request into a fabricated live response. If the actual recording differs, update the script to match exactly.

## Tests

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m playwright install chromium
python tests/onboarding_smoke.py
```

The 40-row W6-7 test spreadsheet is a separate labelled set, not the original 40-case dataset. Recorded local outputs are in the milestone evidence folder; they are not hosted-model or human-study results. Review semantically, not only by HTTP status.

## Team actions still required

1. Record `Academic_Writing_Coach_W6-7_Demo.mp4` yourself, 3–5 minutes.
2. Put the four named submission files and the MP4 in your existing Drive folder's `Week 6-7` subfolder. Drive uploads are handled by the team, not this project update. Do not submit ZIP/RAR.
3. Add actual Week 6/7 prompt history and review changes. Missing historical prompts are not reconstructed as fact.
4. Each member must make at least one genuine commit from their own account. This assisted upload is not proof of three members' contributions. Never backdate history.
5. The user reports a deadline exception and says submission is Tuesday 24 November 2026. Confirm the exact time with your instructor; preserve real file/commit timestamps.
