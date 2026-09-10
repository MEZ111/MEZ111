# Recon Evidence

Recon Evidence turns newline-delimited JSON from reconnaissance tools into a
deduplicated, prioritized, auditable report. It is designed for the point where
raw tool output becomes too noisy to review reliably.

## Why it exists

Security tooling can produce the same observation more than once and with
different field layouts. Recon Evidence normalizes targets, extracts common
fields, creates stable fingerprints, rejects malformed input, and orders the
remaining evidence for human triage.

The score is a review priority. It is deliberately not presented as proof of a
vulnerability.

## Features

- Parses JSONL without third-party dependencies.
- Handles common `url`, `host`, `input`, `matched-at`, and Nuclei `info` fields.
- Normalizes URLs and strips query strings to reduce accidental data exposure.
- Deduplicates observations using stable SHA-256 fingerprints.
- Produces Markdown for human review or JSON for another pipeline.
- Supports strict mode for CI and ingestion jobs.
- Includes deterministic unit tests and sanitized sample data.

## Requirements

- Python 3.9 or newer

## Run it

```bash
git clone https://github.com/MEZ111/MEZ111.git
cd MEZ111/projects/recon-evidence
python3 recon_evidence.py sample.jsonl -o report.md
```

For machine-readable output:

```bash
python3 recon_evidence.py sample.jsonl --format json
```

Fail a CI job when input contains malformed lines:

```bash
python3 recon_evidence.py findings.jsonl --strict
```

## Example

```text
# Recon Evidence Report

Unique observations: 3 · Rejected lines: 0

| Score | Severity | Target                            | Finding                |
| ----: | -------- | --------------------------------- | ---------------------- |
|    70 | medium   | https://portal.example.test/debug | Debug endpoint exposed |
```

## Input contract

Each line must be a JSON object. Recon Evidence intentionally accepts a small,
transparent set of common fields instead of silently guessing every vendor
format.

```json
{"tool":"nuclei","matched-at":"https://portal.example.test/debug","info":{"name":"Debug endpoint exposed","severity":"medium"},"confidence":80}
```

## Scoring

The deterministic score combines severity, supplied confidence, and whether the
observation is exposed over HTTP. Scores are capped at 100. Change the weights in
`SEVERITY_WEIGHT` if your review process uses a different policy.

## Verification

```bash
python3 -m unittest -v test_recon_evidence.py
```

The test suite covers URL normalization, deduplication, ordering, and malformed
input handling.

## Limitations

- The parser does not confirm exploitability or replace manual validation.
- Tool-specific fields outside the documented input contract may remain only in
  compact evidence text.
- The program reads one local file at a time and does not execute scanners.

## Responsible use

Use this program only with systems you own or are explicitly authorized to test.
Sanitize reports before sharing them.

## License

[MIT](../../LICENSE)
