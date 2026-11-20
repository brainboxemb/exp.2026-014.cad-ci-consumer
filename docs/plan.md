# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current goal

Complete the acceptance-overhead maintenance batch for #34 and #35.

The complete external suite is authoritative on pull requests. A manual
`workflow_dispatch` remains available when the same suite genuinely needs to
be run against main. A normal merge to main must not automatically repeat the
entire black-box suite.

Generated-branch publication remains part of `publish_case`, but that case
must use an isolated local bare Git remote. It must not update this repository's
real `build` or `gh-pages` branches and therefore must not trigger a
repository Pages deployment.

The branch will also accept the next exact released `tool.cad.ci` maintenance
stack before merge, so release acceptance and repository housekeeping require
one full-suite PR run.

## Execution order

1. Make pull-request acceptance the one automatic full-suite event.
2. Keep `workflow_dispatch` as an explicit main/manual acceptance path.
3. Remove automatic full acceptance on `push` to main.
4. Change `publish_case` to create an isolated bare remote and work clone.
5. Run real `publish build`, `publish pages`, fetch and cleanup operations
   against that isolated remote.
6. Remove repository write permission from the acceptance workflow.
7. After the combined tool maintenance release exists, pin that exact revision
   in this same branch.
8. Run the complete suite once on the PR, merge, and confirm no automatic full
   acceptance or Pages deployment is triggered by the merge.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #34 Stop publishing an unused repository Pages site | now | Keep publication semantics under test, but move all generated-branch writes to an isolated local remote. |
| #35 Avoid running the full external acceptance suite twice for one change | now | Full suite becomes PR-authoritative; main remains manually testable with workflow_dispatch. |

## Boundary

This repository continues to test released behavior from outside. Local Git
remote setup is test isolation only; it must not implement CAD-CI publication
semantics itself.
