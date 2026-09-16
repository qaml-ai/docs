#!/usr/bin/env python3
"""Weekly camelStream fleet floor check.

Reads the floor definition and the fleet table from stream/fleet.mdx, fetches
each model's Artificial Analysis Intelligence Index score, checks that the live
sales site mirrors the docs, and opens or updates a GitHub issue labeled
`fleet-check` when something is wrong. A later clean run closes the issue.

    python3 scripts/fleet_floor_check.py --dry-run          # report only
    python3 scripts/fleet_floor_check.py --page other.mdx   # parse another file

Exit code 1 means the check itself could not run (page structure changed,
network failure, docs unreachable). Findings about the fleet exit 0; the
GitHub issue is the record for those.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date

REPO = os.environ.get("GITHUB_REPOSITORY", "qaml-ai/docs")
LABEL = "fleet-check"
FLEET_PAGE = "stream/fleet.mdx"
SALES_URL = "https://camelai.com/stream"
DOCS_URL = "https://camelai.com/docs/stream/fleet"
AA_MODEL_URL = "https://artificialanalysis.ai/models/{slug}"
TB_URL = "https://www.tbench.ai/leaderboard/terminal-bench/2.1"
UA = "Mozilla/5.0 (compatible; camelStream-fleet-check; +https://camelai.com/docs/stream/fleet)"

INFRA = {"PAGE STRUCTURE", "NETWORK", "DOCS UNREACHABLE"}


def fetch(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def section(text, heading):
    start = text.find(heading)
    if start < 0:
        return ""
    rest = text[start + len(heading):]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def parse_docs(text, findings):
    floor = section(text, "## The intelligence floor")
    fleet = section(text, "## The current fleet")
    tb = re.search(r"(\d+)%\s+on\s*\[Terminal-Bench 2\.1\]", floor)
    aa = re.search(r"(\d+)\s+on\s+the\s*\[Artificial Analysis Intelligence Index\]", floor)
    ver = re.search(r"\(v(\d+\.\d+)\)", floor)
    verified = re.search(r"_Floor verified against (.+?)_", floor, re.S)
    if not floor:
        findings.append(("PAGE STRUCTURE", "Could not find the `## The intelligence floor` section."))
    if not tb:
        findings.append(("PAGE STRUCTURE", "Could not read the Terminal-Bench 2.1 threshold from the floor section."))
    if not aa:
        findings.append(("PAGE STRUCTURE", "Could not read the Artificial Analysis Intelligence Index threshold from the floor section."))
    if not ver:
        findings.append(("PAGE STRUCTURE", "Could not read the index version, expected as `(vX.Y)` right after the Artificial Analysis Intelligence Index link."))
    if not verified:
        findings.append(("PAGE STRUCTURE", "Could not find the `_Floor verified against ..._` line."))
    models = []
    for line in fleet.splitlines():
        if not line.startswith("| "):
            continue
        m = re.search(r"artificialanalysis\.ai/models/([a-z0-9-]+)", line)
        if not m:
            continue
        models.append((line.split("|")[1].strip(), m.group(1)))
    if not models:
        findings.append(("PAGE STRUCTURE", "Could not find any fleet table rows with an artificialanalysis.ai/models link."))
    return {
        "tb": int(tb.group(1)) if tb else None,
        "aa": int(aa.group(1)) if aa else None,
        "version": ver.group(1) if ver else None,
        "verified": " ".join(verified.group(1).split()).rstrip(".") if verified else None,
        "models": models,
    }


def parse_aa(html, slug):
    title = re.search(r"<title>([^<]*)</title>", html)
    title = title.group(1).strip() if title else ""
    score = re.search(
        r'"label":"([^"]+)","artificialAnalysisIntelligenceIndex":([0-9.]+),"detailsUrl":"/models/%s"'
        % re.escape(slug),
        html,
    )
    ver = re.search(r"Intelligence Index v(\d+\.\d+)", html)
    return {
        "title": title,
        "label": score.group(1) if score else None,
        "raw": float(score.group(2)) if score else None,
        "version": ver.group(1) if ver else None,
    }


def check_models(docs, findings):
    rows = []
    for name, slug in docs["models"]:
        url = AA_MODEL_URL.format(slug=slug)
        try:
            status, html = fetch(url)
        except Exception as e:  # network
            findings.append(("NETWORK", f"Could not fetch {url}: {e}"))
            rows.append((name, slug, None, None, None, "not fetched"))
            continue
        info = parse_aa(html, slug)
        if status == 404 or info["title"] == "Artificial Analysis":
            findings.append(("MISSING SLUG", f"`{slug}` no longer exists on Artificial Analysis (HTTP {status}). Update the link on the fleet page."))
            rows.append((name, slug, None, None, info["version"], "slug missing"))
            continue
        if info["raw"] is None:
            findings.append(("PAGE STRUCTURE", f"Could not find the score for `{slug}` in the Artificial Analysis page HTML; their page format may have changed."))
            rows.append((name, slug, None, None, info["version"], "score not found"))
            continue
        rounded = int(round(info["raw"]))
        if docs["version"] and info["version"] and info["version"] != docs["version"]:
            findings.append(("INDEX VERSION CHANGE", f"Artificial Analysis now publishes index v{info['version']}; the docs floor was set against v{docs['version']}."))
        if docs["aa"] is not None and rounded >= docs["aa"]:
            verdict = f"pass (AA {rounded} >= {docs['aa']})"
        elif docs["aa"] is not None:
            verdict = f"BELOW AA threshold ({rounded} < {docs['aa']}); Terminal-Bench 2.1 leg needs a manual check"
            findings.append(("BELOW FLOOR", f"{name} scores {rounded} on the AA Intelligence Index, below {docs['aa']}. The Terminal-Bench 2.1 leg ({docs['tb']}%) cannot be verified automatically; check {TB_URL}."))
        else:
            verdict = "threshold unknown"
        rows.append((name, slug, info["label"], rounded, info["version"], verdict))
    return rows


def check_sales_site(docs, findings):
    try:
        status, html = fetch(SALES_URL)
    except Exception as e:
        findings.append(("NETWORK", f"Could not fetch {SALES_URL}: {e}"))
        return "not fetched"
    if status != 200:
        findings.append(("NETWORK", f"{SALES_URL} returned HTTP {status}."))
        return f"HTTP {status}"
    aa_nums = sorted(set(re.findall(r"(\d+) or higher on the (?:AA|Artificial Analysis) Intelligence Index", html)))
    tb_nums = sorted(set(re.findall(r"(\d+)% or higher on Terminal-Bench 2\.1", html)))
    if not aa_nums and not tb_nums:
        findings.append(("PAGE STRUCTURE", "The sales site no longer contains the floor phrases this check looks for."))
        return "floor phrase not found"
    drift = []
    if docs["aa"] is not None and any(int(n) != docs["aa"] for n in aa_nums):
        drift.append(f"AA index {', '.join(aa_nums)} on the site vs {docs['aa']} in the docs")
    if docs["tb"] is not None and any(int(n) != docs["tb"] for n in tb_nums):
        drift.append(f"Terminal-Bench {', '.join(tb_nums)}% on the site vs {docs['tb']}% in the docs")
    if drift:
        findings.append(("SALES SITE DRIFT", "; ".join(drift) + ". Update `INTELLIGENCE_FLOOR` in `app/lib/stream-guarantees.ts` (qaml-ai/camelai-salessite) or the docs so they match."))
        return "drift: " + "; ".join(drift)
    return f"matches the docs (AA {', '.join(aa_nums) or '-'}; TB {', '.join(tb_nums) or '-'}%)"


def check_docs_live(findings):
    try:
        status, _ = fetch(DOCS_URL)
    except Exception as e:
        findings.append(("DOCS UNREACHABLE", f"Could not fetch {DOCS_URL}: {e}"))
        return "not fetched"
    if status != 200:
        findings.append(("DOCS UNREACHABLE", f"{DOCS_URL} returned HTTP {status}."))
    return f"HTTP {status}"


def build_report(today, docs, rows, sales, docs_live, findings):
    lines = [f"## Fleet floor check, {today}", ""]
    lines.append(f"Docs floor: {docs['tb']}% on Terminal-Bench 2.1 or {docs['aa']} on the AA Intelligence Index (v{docs['version']}). "
                 f"Floor verified against {docs['verified'] or 'unknown'}.")
    lines += ["", "| Model | AA slug | AA label | AA score | Index version | Verdict |", "| --- | --- | --- | --- | --- | --- |"]
    for name, slug, label, score, ver, verdict in rows:
        lines.append(f"| {name} | `{slug}` | {label or '-'} | {score if score is not None else '-'} | {('v' + ver) if ver else '-'} | {verdict} |")
    lines += ["", f"Sales site (camelai.com/stream): {sales}.", f"Docs page (camelai.com/docs/stream/fleet): {docs_live}.", ""]
    if findings:
        lines.append("### Findings")
        for kind, detail in findings:
            lines.append(f"- **{kind}**: {detail}")
        lines += ["", "### What to do"]
        kinds = {k for k, _ in findings}
        if "INDEX VERSION CHANGE" in kinds:
            lines.append("- Re-check every fleet model on the new index version, then re-baseline the floor together on the docs fleet page (`stream/fleet.mdx`, including the version and the verified line), the invariant line in the docs `CLAUDE.md`, and `INTELLIGENCE_FLOOR` in `app/lib/stream-guarantees.ts` in qaml-ai/camelai-salessite.")
        if "BELOW FLOOR" in kinds:
            lines.append("- For a model below the floor, decide whether to remove it from the fleet or restate the floor, and check its Terminal-Bench 2.1 result by hand first.")
        if "SALES SITE DRIFT" in kinds:
            lines.append("- Deploy the sales site with the same numbers as the docs, or fix whichever side is wrong.")
        if "MISSING SLUG" in kinds:
            lines.append("- Fix the Artificial Analysis link on the fleet page.")
        if kinds & INFRA:
            lines.append("- The check itself could not complete. If the page or site structure changed on purpose, update `scripts/fleet_floor_check.py` to match.")
    else:
        lines.append("All clear: every fleet model clears the floor, the index version is unchanged, and the sales site matches the docs.")
    lines += ["", "_Automated by `.github/workflows/fleet-floor-check.yml`._"]
    return "\n".join(lines)


def gh(method, path, body=None):
    token = os.environ["GITHUB_TOKEN"]
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        "https://api.github.com" + path,
        method=method,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"null")


def ensure_label():
    status, _ = gh("GET", f"/repos/{REPO}/labels/{LABEL}")
    if status == 404:
        gh("POST", f"/repos/{REPO}/labels", {"name": LABEL, "color": "D93F0B", "description": "Automated weekly fleet floor check"})


def open_issue():
    status, issues = gh("GET", f"/repos/{REPO}/issues?labels={LABEL}&state=open&per_page=10")
    if status != 200:
        raise RuntimeError(f"Could not list issues: HTTP {status} {issues}")
    issues = [i for i in issues if "pull_request" not in i]
    return issues[0] if issues else None


def notify(today, report, findings):
    ensure_label()
    existing = open_issue()
    if findings:
        if existing:
            gh("POST", f"/repos/{REPO}/issues/{existing['number']}/comments", {"body": report})
            return f"commented on #{existing['number']} ({existing['html_url']})"
        kinds = sorted({k for k, _ in findings})
        title = f"Fleet floor check: {', '.join(kinds).lower()} ({today})"
        status, issue = gh("POST", f"/repos/{REPO}/issues", {"title": title, "body": report, "labels": [LABEL]})
        if status != 201:
            raise RuntimeError(f"Could not create issue: HTTP {status} {issue}")
        return f"opened #{issue['number']} ({issue['html_url']})"
    if existing:
        gh("POST", f"/repos/{REPO}/issues/{existing['number']}/comments", {"body": report})
        gh("PATCH", f"/repos/{REPO}/issues/{existing['number']}", {"state": "closed", "state_reason": "completed"})
        return f"all clear; closed #{existing['number']}"
    return "all clear; no issue needed"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print the report without touching GitHub")
    ap.add_argument("--page", default=FLEET_PAGE, help="fleet page to parse (default: stream/fleet.mdx)")
    args = ap.parse_args()

    today = date.today().isoformat()
    findings = []
    with open(args.page, encoding="utf-8") as f:
        docs = parse_docs(f.read(), findings)
    rows = check_models(docs, findings)
    sales = check_sales_site(docs, findings)
    docs_live = check_docs_live(findings)
    report = build_report(today, docs, rows, sales, docs_live, findings)

    print(report)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(report + "\n")

    if args.dry_run:
        print(f"\n[dry run] {len(findings)} finding(s); GitHub not touched.")
    else:
        print("\n" + notify(today, report, findings))

    infra = [k for k, _ in findings if k in INFRA]
    sys.exit(1 if infra else 0)


if __name__ == "__main__":
    main()
