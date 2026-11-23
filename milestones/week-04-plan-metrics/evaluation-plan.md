# Evaluation plan and blank observation record

No human usability study has been run for this package. Do not invent participants or results.

| Objective | Target | Method |
|---|---|---|
| O1 AI/source quality | ≥90% rule and citation accuracy | Independent reviewer opens every source, confirms feedback support; then held-out prompts, incorrect-source count / all source claims |
| O2 Task success | ≥80% independent revisions | At least five peers try fictional tasks; score against a prewritten rubric, without the coach rewriting |
| O3 Transparency | ≥90% correct distinction | Ask participants to classify Mandatory rule vs Style suggestion and explain source/evidence limits |
| O4 Latency | Mean UI submission-to-display <2 seconds | Measure browser timings by provider, include normal responses and separately report retry/error paths |
| O5 Uncertainty | ≥95% correct handling | At least 20 held-out missing-context/conflict/unverifiable-source tasks; require no confident unsupported diagnosis |

## Study procedure

Obtain consent. Do not collect names, screenshots containing personal details, real drafts, or account secrets. Assign random fictional participant IDs P01–P05. Include a novice task, citation task, suggestion task, uncertainty task, keyboard task, and handover task. Have the participant revise synthetic text independently. Use a SUS questionnaire after the tasks with the standard scoring procedure; do not treat a custom one-question rating as SUS.

## Record template

| Participant ID | Task ID | Success / failure | Time | Label classification | Difficulty note (no personal data) |
|---|---|---|---|---|---|
| Pending | Pending | Not tested | | | |

Automated fixture results are stored separately. Reusing the dataset's labelled prompts tests implementation consistency, not generalization. Additional paraphrased and adversarial cases should be reviewed independently before making accuracy claims.
