# AI Vendor Risk Assessment Kit (Questionnaire + Scoring + Report)

A practical toolkit to run AI vendor due diligence in a repeatable way:
- A **question bank** (YAML) + human-friendly questionnaire (Markdown)
- A **scoring rubric** across key risk domains
- A **report generator** producing an executive summary + findings + guardrails

This is designed as a portfolio project for AI Governance / GRC work.

## Risk domains
1. Use case fit
2. Business integration
3. Use of confidential data
4. Business resiliency
5. Potential for exposure

## Quickstart
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/score_[vendor.py](http://vendor.py) --responses examples/vendor_responses_risky.json

This produces:
- `out/vendor_report.md`

## Repo structure
questionnaires/
- vendor_ai_security_[privacy.md](http://privacy.md)
- question_bank.yaml
rubric/
- scoring_rubric.yaml
- scripts/
- score_[vendor.py](http://vendor.py)
examples/
- vendor_responses_good.json
- vendor_responses_risky.json
out/
- (generated reports go here)

## Output
- Executive decision: **Accept / Accept with guardrails / Reject**
- Domain score breakdown
- Findings and recommended controls
- Evidence checklist (what to request from the vendor)

## License
MIT
