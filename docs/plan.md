# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current goal

Complete one combined maintenance/acceptance batch for #34, #35 and #36.

The exact external target is released `tool.cad.ci 0.12.0` at
`05af21546ea71907cd9db4b56f5d5ccd644c0170`, which pins released `lib.py.cad.ci 0.7.0`.

The same PR also makes the acceptance repository cheaper and cleaner:

- one automatic complete suite on pull requests;
- explicit `workflow_dispatch` for exceptional main verification;
- no automatic complete rerun after merge;
- real generated-branch publication tested against an isolated local bare
  remote rather than this repository's real `build` / `gh-pages` branches.

## Execution order

1. Pin exact released tool 0.12.0 in both manifest and reusable workflow.
2. Accept library 0.7.0 evidence schemas/timestamps from outside.
3. Accept high-level concurrency and lower-level independence from outside.
4. Run all existing black-box behavior, including publication, against the
   exact released stack.
5. Keep publication branch writes isolated to the runner-local remote.
6. Merge only after the one complete pull-request acceptance is green.
7. Confirm the merge does not automatically trigger a second complete
   acceptance run.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #34 Stop publishing an unused repository Pages site | now | Preserve publication acceptance, but direct generated branches to an isolated local remote instead of the real repository. |
| #35 Avoid running the full external acceptance suite twice for one change | now | Pull-request acceptance is authoritative; workflow_dispatch remains the explicit main verification path. |
| #36 Accept tool.cad.ci 0.12.0 maintenance release | now | Exact released stack accepted in this same maintenance PR so only one complete suite is required. |

## Boundary

The repository remains a black-box consumer. Event policy and local Git-remote
setup are test infrastructure only; generic CAD-CI behavior remains in the
released tool/library stack.
