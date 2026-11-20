# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released `tool.cad.ci` 0.14.1 is available at exact commit
`18812d38e2390c23fd3c431cfde2ce9367bdfd40`.

It retains the single-runner PR lifecycle from 0.14.0 and optimizes only fixed
hosted-runner bootstrap work: shallow caller checkout, exact base fetch, direct
Docker CLI GHCR login and lighter external dependency installation.

The tool still pins released `lib.py.cad.ci` 0.8.3 at exact commit
`e8e951ed7e50c4fa754cc158729faf2927cccb31`.

## Current goal

Complete #54 by externally accepting released tool.cad.ci 0.14.1 before Forge
adopts it.

## Required proof

- exact released 0.14.1 revision is pinned everywhere;
- the complete reusable PR workflow remains one runner;
- the caller checkout is shallow and fetches only the exact base SHA needed for
  incremental selection;
- docker/login-action is absent and direct Docker CLI login is present;
- external dependency install uses --no-deps --no-compile;
- no persistent Actions cache appears;
- every existing black-box execution/selection/publication/logging case remains
  green.

## Execution order

1. Pin exact released tool 0.14.1.
2. Extend maintenance acceptance for the optimized reusable PR bootstrap.
3. Run the complete external suite.
4. Merge only after every job is green.
5. Only then update Forge's PR workflow pin.
6. Repeat the same simple-box-only end-to-end measurement.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #54 Accept tool.cad.ci 0.14.1 PR bootstrap optimization | now | Required released-stack proof before the next Forge timing measurement. |

## Boundary

This repository observes released behavior only. Generated-branch acceptance
remains isolated from the repository's real build/gh-pages branches.
