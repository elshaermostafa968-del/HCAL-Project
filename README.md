# HCAL Project: Academic Writing Coach

A university writing-assistant prototype built around the HAI principle of **Transparency**.

## Milestones

| Folder | Contents |
|---|---|
| `milestones/week-03-users-data/` | Three fictional personas, bias review, source/permission notes, 40 synthetic cases, report PDF and editable Markdown |
| `milestones/week-04-plan-metrics/` | Persona journey maps, five measurable targets, Transparency ladder, evaluation plan, blank study records, report PDF and Markdown |
| `milestones/week-06-07/` | Milestone 3 design pack, test workbook, exact demo script, prompt-log record, and revised onboarding chatbot |
| `milestones/week-05-chatbot/` | Runnable FastAPI + HTML/CSS/JS chatbot, full dataset, diagrams, report, tests, local evidence, and live-response capture script |

## Run the chatbot

For the current Milestone 3 demo use `milestones/week-06-07/chatbot/`. The Week 5 version remains separately preserved. From the selected chatbot folder, use Python 3.10 or newer:

```sh
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload
```

Open http://127.0.0.1:8000. The default local mode needs no API key and is explicitly labelled **not a live model**. See the Week 5 README for Gemini/OpenAI configuration and `scripts/first_call.py`.

## Honest submission status

- The runnable local demo, 40-case fixture evaluation, unit tests, and browser smoke checks are included.
- A successful hosted-model response still requires the team's own working API key. No live reply has been fabricated.
- The strict model contract returns only approved case feedback and hints. This is a small extractive teaching prototype, not a general writing engine.
- Human usability results, missing historical exact prompts, and the team's licensing decision must be completed by the team. Targets are not claimed results.
- All sample drafts and bibliographic examples are fictional. Never commit API keys or real student data.

## Repository cleanup

The six earlier root-level report/presentation files were replaced by the organized milestone folders in a single update. Their original versions remain available in Git history. The Google Drive folder is a separate destination and was not changed by this repository update.
