# Contribution standards

This repository contains the MEZ111 profile and reusable documentation materials.
It is not an installable application.

## Changes

1. Read the affected document and keep claims factual.
2. Make one focused change per commit.
3. Check relative links and preview the Markdown.
4. Open a pull request explaining the problem, the change, and verification.

## Commit messages

Use `type(optional-scope): imperative description`.

- `feat:` adds a capability.
- `fix:` corrects a bug.
- `docs:` changes documentation.
- `refactor:` restructures code without changing behavior.
- `test:` adds or updates tests.
- `chore:` maintains repository tooling.

Examples:

```text
docs(profile): clarify technical focus
fix(parser): reject malformed input
feat(cli): add JSON output option
```

Describe what actually changed. Do not claim a vulnerability was fixed without
evidence. Keep existing published history intact; use this convention for new
commits.

## Publishing projects

Use [the project README template](templates/PROJECT_README.md) as a starting point.
Replace every placeholder, verify commands, and include real output.
Choose a license for each project based on ownership and dependency requirements;
this repository's MIT license does not automatically license other repositories.

Add a language-specific .gitignore for each code project. Ignoring a file does not
remove it from Git history or stop tracking an already committed file.

## External contributions

Follow the target project's CONTRIBUTING instructions and license. Reproduce the
issue, check for an existing fix, make the smallest useful change, and run the
relevant tests. A submitted pull request is not a merged contribution.
