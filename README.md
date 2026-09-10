<p align="center">
  <img src="assets/header.svg" width="100%" alt="MEZ111 — security, automation, and systems">
</p>

<p align="center">
  <a href="projects/recon-evidence/README.md"><img alt="Flagship project" src="https://img.shields.io/badge/FLAGSHIP-Recon%20Evidence-34d399?style=for-the-badge&labelColor=07120f"></a>
  <a href="projects/recon-evidence/test_recon_evidence.py"><img alt="Tests" src="https://img.shields.io/badge/TESTS-3%20PASSING-a7f3d0?style=for-the-badge&labelColor=07120f"></a>
  <a href="SECURITY.md"><img alt="Responsible disclosure" src="https://img.shields.io/badge/SECURITY-RESPONSIBLE%20DISCLOSURE-6ee7b7?style=for-the-badge&labelColor=07120f"></a>
</p>

## I turn noisy technical output into evidence people can act on.

I build security and automation tools with three requirements: the result must be reproducible, the interface must be clear, and every claim must be inspectable in the code.

<div dir="rtl">

أبني أدوات أمنية وبرمجية تحوّل النتائج المبعثرة إلى معلومات واضحة قابلة للمراجعة واتخاذ القرار.

</div>

## Featured build — Recon Evidence

Raw reconnaissance output is repetitive, inconsistent, and difficult to audit. **Recon Evidence** is a dependency-free Python CLI that normalizes JSONL from common security tools, removes duplicate observations using stable fingerprints, prioritizes evidence, and produces reports for humans or pipelines.

<table>
<tr>
<td width="50%">

**Input**

```json
{"tool":"nuclei",
 "matched-at":"https://portal.example.test/debug",
 "info":{"name":"Debug endpoint exposed",
         "severity":"medium"},
 "confidence":80}
```

</td>
<td width="50%">

**Output**

```text
score     70
severity  medium
target    /debug
status    prioritized
```

</td>
</tr>
</table>

- **Verified:** 3 deterministic unit tests pass.
- **Auditable:** scoring is explicit and capped; malformed lines are reported.
- **Private by design:** query strings are removed during normalization.
- **Safe boundary:** the program processes local evidence and never executes scanners.

[Read the design and run it →](projects/recon-evidence/README.md) · [Inspect the source →](projects/recon-evidence/recon_evidence.py) · [Review the tests →](projects/recon-evidence/test_recon_evidence.py)

## Working stack

| Area | Tools | What I use them for |
| --- | --- | --- |
| Security | Burp Suite, Nmap, Wireshark, Nuclei | validation, traffic analysis, asset evidence |
| Automation | Python, JSON, CLI workflows | normalization, repeatable processing, reporting |
| Applications | Flutter, React, Supabase | product interfaces and data-backed applications |
| Delivery | Git, GitHub, Linux | versioned changes, review, reproducible execution |

## Engineering standards

```text
scope before scanning
evidence before severity
tests before claims
clear limits before release
```

Every public project should include a tested setup path, real usage, sanitized output, known limitations, a fitting license, and a security boundary. New work follows Conventional Commits so the history explains why the code changed.

## Activity

<p>
  <a href="https://github.com/MEZ111?tab=repositories"><img alt="Repositories" src="https://img.shields.io/badge/EXPLORE-REPOSITORIES-ecfdf5?style=for-the-badge&labelColor=102720"></a>
  <a href="https://github.com/MEZ111?tab=overview"><img alt="Contribution history" src="https://img.shields.io/badge/VIEW-CONTRIBUTION%20HISTORY-ecfdf5?style=for-the-badge&labelColor=102720"></a>
</p>

---

<sub><a href="SECURITY.md">Security policy</a> · <a href="CONTRIBUTING.md">Contribution standards</a> · <a href="templates/PROJECT_README.md">Project documentation template</a></sub>
