# Evidence status

- `desktop-start.png`, `desktop-feedback.png`, `mobile-start.png`, and `handover.png` show the actual local demo in an automated Chromium session.
- The PDF preview images are layout-check evidence, not test-participant screenshots.
- `eval/results/` contains actual labelled local fixture outputs and metrics. Reusing training fixtures is not held-out accuracy.
- No real hosted-model response was obtained because the team has not supplied a key. Run `python scripts/first_call.py` after configuring a real provider. The script will not save local output as live evidence.
- Provider-success tests use simulated HTTP responses and are not live-model evidence.
