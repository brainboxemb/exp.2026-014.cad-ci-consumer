# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released `tool.cad.ci 0.15.0` remains the currently accepted stack.

Forge #572 requires long-lived named development scopes. Generic behavior is
being added in `lib.py.cad.ci` #72 and exposed by `tool.cad.ci` #80.

## Current goal

Complete #60 as soon as the exact #80 tool release exists.

The black-box acceptance must prove that one released stack can safely maintain
multiple independent complete build scopes and Pages subtrees.

## Required proof

- publish complete `main`, `dev_a` and `dev_b` build scopes;
- update `dev_a` and preserve `main` + `dev_b`;
- publish stable Pages plus `dev_a` and `dev_b` subtrees;
- replace `dev_a` while preserving stable root + `dev_b`;
- replace stable root while preserving both named subtrees;
- reject unsafe names;
- use only the released public tool/library surface;
- keep publication tests isolated from this repository's real generated branches.

## Execution order

1. [lib.py.cad.ci #72] Generic named-scope implementation/release.
2. [tool.cad.ci #80] Thin exposure/release.
3. [#60, blocked until #80] Pin that exact tool revision.
4. [#60] Run complete black-box named-scope acceptance.
5. [Forge #572] Adopt the accepted stack and create `dev_cad` / `dev_ci`.

## Open issue assessment — 2026-11-21

| Issue | Status | Assessment |
| --- | --- | --- |
| #60 Accept released named build and Pages scopes | blocked on tool #80 | Required external proof before Forge creates its two long-lived development lanes. |

Immediate chain:

`lib #72 -> tool #80 -> acceptance #60 -> Forge #572`.
