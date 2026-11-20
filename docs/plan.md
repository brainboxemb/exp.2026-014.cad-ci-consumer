# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

The previously accepted stack is `tool.cad.ci` 0.12.1 with
`lib.py.cad.ci` 0.7.1.

Released `tool.cad.ci` 0.12.2 is available at exact commit
`8bab91eaf8554533e5f63620421ed9554f66eb91`.

0.12.2 changes only reusable-workflow artifact transport when a successful run
materializes no `build/` output.

## Current goal

Complete #38 as black-box acceptance of exact released tool 0.12.2.

Prove both artifact paths:

- normal materialized output remains downloadable with hidden `.cad-ci`
  evidence;
- a valid no-output run with `upload_build: true` succeeds and exposes an empty
  artifact name.

## Execution order

1. Pin exact released tool 0.12.2 in `dependencies.repos`.
2. Pin the same exact commit in the reusable workflow call.
3. Preserve the existing full-run artifact/evidence acceptance.
4. Add one incremental no-output reusable-workflow call for the PR itself.
5. Assert that no-output call succeeds and returns an empty artifact name.
6. Run the complete external acceptance suite on the PR.
7. Merge only after the full suite is green.
8. Only then allow Forge to pin tool 0.12.2.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #38 Accept tool.cad.ci 0.12.2 optional build artifact transport | now | Exact released-stack acceptance required before Forge adoption. |

## Boundary

This repository observes the released workflow from outside. It does not
reimplement selection, build output detection or artifact transport.
