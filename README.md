<p align="center">
  <img src="assets/header.svg" width="100%" alt="MEZ111 — security, automation, and systems">
</p>

<p align="center">
  <strong>Security engineering through explainable systems.</strong><br>
  Detection logic, static analysis, attack-surface intelligence, and reproducible automation.
</p>

<p align="center">
  <a href="https://github.com/MEZ111/surface-delta"><img src="https://img.shields.io/github/actions/workflow/status/MEZ111/surface-delta/verify.yml?branch=main&style=flat-square&label=surface-delta" alt="SurfaceDelta build"></a>
  <a href="https://github.com/MEZ111/pysinktrace"><img src="https://img.shields.io/github/actions/workflow/status/MEZ111/pysinktrace/verify.yml?branch=main&style=flat-square&label=pysinktrace" alt="PySinkTrace build"></a>
  <a href="https://github.com/MEZ111/beacon-lens"><img src="https://img.shields.io/github/actions/workflow/status/MEZ111/beacon-lens/verify.yml?branch=main&style=flat-square&label=beacon-lens" alt="BeaconLens build"></a>
</p>

---

## Three security problems. Three inspectable engines.

<table>
<tr>
<td width="33%" valign="top">

### [SurfaceDelta](https://github.com/MEZ111/surface-delta)

**Attack-surface drift intelligence**

Compares service snapshots and identifies:

- newly exposed services
- TLS regressions
- private-to-public changes
- software fingerprint drift
- policy-based CI failures

Every score carries its reasons.

</td>
<td width="33%" valign="top">

### [PySinkTrace](https://github.com/MEZ111/pysinktrace)

**Explainable Python taint tracing**

Uses the Python AST to trace:

- web request sources
- assignment propagation
- command and process sinks
- SQL execution paths
- `eval` and `exec` flows
- SARIF output for code scanning

Every finding includes its line path.

</td>
<td width="33%" valign="top">

### [BeaconLens](https://github.com/MEZ111/beacon-lens)

**Network behavior triage**

Analyzes Zeek JSON for:

- recurring connection intervals
- stable outbound payload sizes
- DNS prefix entropy
- uniqueness and length gates
- analyst-readable evidence
- threshold-based CI failures

Every signal exposes its statistics.

</td>
</tr>
</table>

## The design rule

```text
raw telemetry
      ↓ normalize
defensible evidence
      ↓ explain
review priority
      ↓ verify
human decision
```

I build tools around evidence instead of opaque verdicts. Scores are deterministic. Boundaries are documented. Example data is sanitized. Claims are backed by tests and GitHub Actions.

<div dir="rtl">

أبني أدوات أمنية تشرح كيف وصلت للنتيجة؛ من البيانات الخام، إلى الدليل، إلى سبب رفع الأولوية. كل مشروع قابل للتشغيل والمراجعة والاختبار.

</div>

## Engineering surface

| Layer | Work |
| --- | --- |
| Application security | source-to-sink analysis, input propagation, SARIF |
| Exposure intelligence | service inventory, snapshot comparison, security drift |
| Network detection | timing analysis, payload stability, DNS entropy |
| Automation | installable Python CLIs, JSONL pipelines, Markdown/JSON output |
| Delivery | deterministic tests, GitHub Actions, scoped permissions, documented limits |

## Verification

The three independent repositories currently contain **10 deterministic tests** plus install-and-run CI workflows.

```bash
surface-delta before.jsonl after.jsonl --fail-risk 70
pysinktrace src/ --format sarif -o results.sarif
beacon-lens zeek.jsonl --json
```

### Additional lab

[Recon Evidence](projects/recon-evidence/README.md) normalizes and deduplicates mixed reconnaissance output into an auditable triage report.

---

<p align="center">
  <a href="SECURITY.md">Security policy</a> ·
  <a href="CONTRIBUTING.md">Contribution standards</a> ·
  <a href="https://github.com/MEZ111?tab=repositories">All repositories</a>
</p>
