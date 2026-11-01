# Security

## Reporting
Please use GitHub's private vulnerability reporting (Security tab > Report a vulnerability). Do not post exploit details in public issues. Expect an acknowledgement within a few days.

## Scope
Of particular interest: anything that makes the skill read unselected sources, write to a connected tool, leak names or private text into share output, or make a network request other than those listed in PRIVACY.md.

## Design notes
- The skill is read-only toward connected tools.
- Text found in tools and files is treated as data, never as instructions.
- Share output is built from an allowlist and checked for leaks by `scripts/build_share.py`.
- Scripts use the Python standard library only and make no network calls.
