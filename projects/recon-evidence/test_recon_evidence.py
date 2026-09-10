import unittest

from recon_evidence import load_jsonl, normalize_target


class ReconEvidenceTests(unittest.TestCase):
    def test_normalizes_urls_and_hosts(self):
        self.assertEqual(normalize_target("HTTPS://Example.COM/path/?x=1"), "https://example.com/path")
        self.assertEqual(normalize_target("EXAMPLE.COM/"), "example.com")

    def test_deduplicates_and_orders_findings(self):
        lines = [
            '{"tool":"nuclei","matched-at":"https://example.com/a","info":{"name":"Header leak","severity":"low"},"confidence":80}',
            '{"tool":"nuclei","matched-at":"https://example.com/a","info":{"name":"Header leak","severity":"low"},"confidence":80}',
            '{"tool":"nuclei","matched-at":"https://example.com/b","info":{"name":"Exposure","severity":"high"},"confidence":90}',
        ]
        findings, errors = load_jsonl(lines)
        self.assertEqual(errors, [])
        self.assertEqual(len(findings), 2)
        self.assertEqual(findings[0].severity, "high")

    def test_reports_invalid_lines(self):
        findings, errors = load_jsonl(["not-json"])
        self.assertEqual(findings, [])
        self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
