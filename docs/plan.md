# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released and externally accepted tool 0.12.2 remains the previous baseline.

Released `tool.cad.ci` 0.12.3 is available at exact commit
`ad7099b4712af13067c1c42ad50e89bf6a8306dd`.

0.12.3 changes only `build prepare-main` translation so an unselected main
candidate uses the released library full-run `process` selection.

## Current goal

Complete #40 as black-box acceptance of exact released tool 0.12.3.

Extend the existing `process_case` to prove:

- full-run execution excludes `process: false` items;
- `build prepare-main` accepts the resulting candidate output;
- the prepared main candidate contains only the active items;
- the disabled item is neither required nor copied.

## Execution order

1. Pin exact released tool 0.12.3 in `dependencies.repos`.
2. Pin the same exact commit in reusable workflow calls.
3. Extend `process_case` with `build prepare-main` acceptance.
4. Run the complete external suite.
5. Merge only after all existing acceptance remains green.
6. Only then allow Forge #366 to pin 0.12.3.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #40 Accept tool.cad.ci 0.12.3 processed main candidate selection | now | Exact released-stack acceptance required before Forge stable-main bootstrap. |

## Boundary

This repository observes the released stack from outside. It does not
reimplement `process`, full-run selection or build-store behavior.
