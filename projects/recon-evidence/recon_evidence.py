#!/usr/bin/env python3
"""Normalize JSONL security-tool output into an auditable evidence report."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlsplit, urlunsplit


SEVERITY_WEIGHT = {
    "critical": 50,
    "high": 35,
    "medium": 20,
    "low": 8,
    "info": 1,
    "unknown": 0,
}


@dataclass(frozen=True)
class Finding:
    fingerprint: str
    tool: str
    target: str
    title: str
    severity: str
    score: int
    evidence: str
    source_line: int


def normalize_target(value: str) -> str:
    value = value.strip()
    if not value:
        return "unknown"
    if "://" not in value:
        try:
            return str(ipaddress.ip_address(value))
        except ValueError:
            return value.lower().rstrip("/")
    parsed = urlsplit(value)
    host = (parsed.hostname or "").lower()
    port = f":{parsed.port}" if parsed.port else ""
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), f"{host}{port}", path, "", ""))


def compact_evidence(record: dict) -> str:
    evidence = record.get("evidence") or record.get("matched-at") or record.get("url")
    if evidence:
        return str(evidence).replace("\n", " ")[:240]
    return json.dumps(record, ensure_ascii=False, sort_keys=True)[:240]


def extract(record: dict, line_number: int) -> Finding:
    info = record.get("info") if isinstance(record.get("info"), dict) else {}
    tool = str(record.get("tool") or record.get("source") or "unknown").lower()
    target = normalize_target(str(
        record.get("target") or record.get("matched-at") or record.get("url")
        or record.get("host") or record.get("input") or "unknown"
    ))
    title = str(record.get("title") or record.get("name") or info.get("name") or "Observed asset")
    severity = str(record.get("severity") or info.get("severity") or "unknown").lower()
    if severity not in SEVERITY_WEIGHT:
        severity = "unknown"
    confidence = record.get("confidence", 50)
    try:
        confidence_value = max(0, min(100, int(confidence)))
    except (TypeError, ValueError):
        confidence_value = 50
    exposure_bonus = 10 if target.startswith(("http://", "https://")) else 0
    score = min(100, SEVERITY_WEIGHT[severity] + confidence_value // 2 + exposure_bonus)
    identity = "\0".join((tool, target, title.lower(), severity))
    fingerprint = hashlib.sha256(identity.encode()).hexdigest()[:12]
    return Finding(
        fingerprint=fingerprint,
        tool=tool,
        target=target,
        title=title,
        severity=severity,
        score=score,
        evidence=compact_evidence(record),
        source_line=line_number,
    )


def load_jsonl(lines: Iterable[str]) -> tuple[list[Finding], list[str]]:
    findings: dict[str, Finding] = {}
    errors: list[str] = []
    for line_number, raw in enumerate(lines, 1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
            if not isinstance(record, dict):
                raise ValueError("expected a JSON object")
            finding = extract(record, line_number)
            findings.setdefault(finding.fingerprint, finding)
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append(f"line {line_number}: {exc}")
    ordered = sorted(findings.values(), key=lambda item: (-item.score, item.target, item.title))
    return ordered, errors


def markdown_report(findings: list[Finding], errors: list[str]) -> str:
    counts = {severity: 0 for severity in SEVERITY_WEIGHT}
    for finding in findings:
        counts[finding.severity] += 1
    lines = [
        "# Recon Evidence Report",
        "",
        f"**Unique observations:** {len(findings)} · **Rejected lines:** {len(errors)}",
        "",
        "| Critical | High | Medium | Low | Info | Unknown |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
        f"| {counts['critical']} | {counts['high']} | {counts['medium']} | {counts['low']} | {counts['info']} | {counts['unknown']} |",
        "",
        "## Prioritized evidence",
        "",
        "| Score | Severity | Target | Finding | Tool | ID |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for item in findings:
        safe = lambda text: str(text).replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {item.score} | {safe(item.severity)} | {safe(item.target)} | "
            f"{safe(item.title)} | {safe(item.tool)} | `{item.fingerprint}` |"
        )
    if errors:
        lines.extend(["", "## Rejected input", ""])
        lines.extend(f"- {error}" for error in errors)
    lines.extend([
        "",
        "> A score orders triage; it does not prove exploitability. Validate every observation manually and stay inside authorized scope.",
        "",
    ])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSONL input from supported security tools")
    parser.add_argument("-o", "--output", type=Path, help="write the report to this path")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--strict", action="store_true", help="exit non-zero when any line is invalid")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        with args.input.open(encoding="utf-8") as stream:
            findings, errors = load_jsonl(stream)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        output = json.dumps({"findings": [asdict(item) for item in findings], "errors": errors}, indent=2)
    else:
        output = markdown_report(findings, errors)

    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
