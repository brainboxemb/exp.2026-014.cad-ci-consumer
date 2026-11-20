# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released `tool.cad.ci` 0.14.0 is available at exact commit
`5bca68eb109a69e3a05e7711daf394926ee0e7d4`.

That tool pins released `lib.py.cad.ci` 0.8.3 at exact commit
`e8e951ed7e50c4fa754cc158729faf2927cccb31`.

The previous 0.13.3 stack already passed streamed execution logging acceptance.

## Current goal

Complete #52 by accepting the released 0.14.0 single-runner PR workflow.

## Required proof

- exact released tool 0.14.0 is pinned in dependencies and reusable workflow calls;
- released `reusable-pr.yml` uses one runner job;
- it has no artifact upload/download handoff;
- it does not editable-install/build tool.cad.ci or lib.py.cad.ci;
- it resolves the exact library source from the tool pin and exposes both source
  roots through `PYTHONPATH`;
- it invokes released prepare-pr, publish and cleanup commands;
- all previous execution, selection, logging and isolated publication cases
  remain green.

## Execution order

1. Pin exact released tool 0.14.0.
2. Extend released-workflow maintenance acceptance for `reusable-pr.yml`.
3. Run the complete external suite.
4. Merge only after all jobs are green.
5. Only then update Forge to exact tool 0.14.0.
6. Measure one normal simple-box Forge PR end-to-end against the <=30 s target.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #52 Accept tool.cad.ci 0.14.0 single-runner PR workflow | now | Required released-stack proof before Forge adoption. |

## Boundary

This repository observes the released workflow/tool/library stack. It does not
implement workflow orchestration, SCons execution or publication mechanics.

Generated-branch publication acceptance remains isolated from this repository's
real build and gh-pages branches.
