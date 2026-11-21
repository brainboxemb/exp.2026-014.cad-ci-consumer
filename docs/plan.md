# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Generic named complete build scopes and named Pages subtrees are released in:

- `lib.py.cad.ci 0.9.2` at
  `3f688243f4ee65b1fa42f82adde5344fe5101775`;
- `tool.cad.ci 0.16.1` at
  `4c6bb8b35009ef5008bd99134cf84b59fddc0b8a`.

The first #60 acceptance run against 0.16.0 correctly exposed a library
self-compatibility defect: current SCons output used engine schema 2 while the
durable build store still expected schema 1. That was fixed in
`lib.py.cad.ci 0.9.2` and repinned by `tool.cad.ci 0.16.1`.

The named-scope acceptance itself remains unchanged.

## Current goal

Complete #60 against exact released `tool.cad.ci 0.16.1`.

The black-box suite must prove that one released stack safely maintains
multiple independent complete build scopes and Pages subtrees before Forge
#572 creates `dev_cad` and `dev_ci`.

## Required proof

- publish complete `main`, `dev_a` and `dev_b` build scopes;
- update `dev_a` and preserve `main` + `dev_b`;
- publish stable Pages plus `dev_a` and `dev_b` subtrees;
- replace `dev_a` while preserving stable root + `dev_b`;
- replace stable root while preserving both named subtrees;
- reject unsafe names;
- use only the exact released public tool/library surface;
- keep publication tests isolated from this repository's real generated branches;
- keep the existing same-runner and reusable-workflow acceptance green.

## Execution order

1. [#60, now] Pin exact released tool.cad.ci 0.16.1.
2. [#60] Run the complete black-box suite including named-scope isolation.
3. Merge only when all released-stack paths are green.
4. [Forge #572] Adopt the accepted stack and introduce `dev_cad` / `dev_ci`.

## Open issue assessment — 2026-11-21

| Issue | Status | Assessment |
| --- | --- | --- |
| #60 Accept released named build and Pages scopes | now | 0.9.2/0.16.1 fix the schema blocker found by the first run; rerun the unchanged named-scope isolation proof now. |

Immediate chain:

`acceptance #60 -> Forge #572`.
