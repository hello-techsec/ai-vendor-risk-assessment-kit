import json
import argparse
import yaml
from pathlib import Path

def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def score(responses, rubric):
    points = 0
    applied = []

    for rule in rubric["rules"]:
        qid = rule["question_id"]
        expected = rule["when"]
        if responses.get(qid) == expected:
            points += rule["add_points"]
            applied.append(rule)

    # Simple decision thresholds (tweak as you like)
    if points >= 7:
        decision = "REJECT"
    elif points >= 3:
        decision = "ACCEPT_WITH_GUARDRAILS"
    else:
        decision = "ACCEPT"

    return points, decision, applied

def render_report(vendor_name, responses, points, decision, applied_rules):
    lines = []
    lines.append(f"# Vendor Risk Assessment Report: {vendor_name}")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append(f"- Decision: **{decision}**")
    lines.append(f"- Total risk points: **{points}**")
    lines.append("")
    lines.append("## Key Findings (Rules Triggered)")
    if not applied_rules:
        lines.append("- No rubric rules were triggered.")
    else:
        for r in applied_rules:
            lines.append(f"- **{r['question_id']}**: {r['rationale']} ( +{r['add_points']} )")
    lines.append("")
    lines.append("## Responses (Snapshot)")
    for k, v in sorted(responses.items()):
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    lines.append("## Suggested Guardrails (if applicable)")
    lines.append("- Require opt-out for training on customer data.")
    lines.append("- Require logging/monitoring access and incident notification SLAs.")
    lines.append("- Confirm data retention/deletion, sub-processors, and cross-border transfer controls.")
    lines.append("")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--responses", required=True)
    args = ap.parse_args()

    rubric = load_yaml("rubric/scoring_rubric.yaml")

    data = json.loads(Path(args.responses).read_text(encoding="utf-8"))
    vendor_name = data.get("vendor_name", "Unknown Vendor")
    responses = data.get("responses", {})

    points, decision, applied = score(responses, rubric)
    report = render_report(vendor_name, responses, points, decision, applied)

    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "vendor_report.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
