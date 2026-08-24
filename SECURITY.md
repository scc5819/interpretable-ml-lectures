# Security Policy

This is a repository of lecture materials — there is no deployed service and no
user data. The plausible security issues are: a malicious or compromised
dependency pin, a compromised GitHub Action, or notebook code that does
something a reader running it locally would not expect.

## Reporting

Please report privately via
[GitHub's private vulnerability reporting](https://github.com/scc5819/interpretable-ml-lectures/security/advisories/new)
— do not open a public issue for anything you believe is exploitable.
Reports are read by the maintainers listed in
[CONTRIBUTING.md](CONTRIBUTING.md#maintainers); expect a first response within a
week (this is a course repository maintained by people with coursework).

## Scope notes

- Dependency versions are pinned in `requirements.txt` and fully resolved with
  hashes in `requirements.lock`; CI actions are pinned to commit SHAs and
  watched by Dependabot (actions ecosystem only).
- Notebooks are meant to be run locally by students: code that touches the
  network beyond `%pip install`, reads files outside the repository, or
  obfuscates what it does is a valid report even if it is not "exploitable".
