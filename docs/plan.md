# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released `tool.cad.ci 0.14.2` is available at exact commit
`4c1016d594368146fb9c16602f01c158e85d9afb`.

That tool pins released `lib.py.cad.ci 0.8.4` and exposes explicit current
processed-item membership to durable main updates.

## Current goal

Complete #56 by externally accepting released tool.cad.ci 0.14.2 before Forge
adopts it.

Extend the existing `publish_case`; do not create a new implementation or
acceptance family.

## Required proof

- exact released 0.14.2 revision is pinned everywhere;
- every existing black-box case remains green;
- a durable main baseline with items A+B can be updated from a current
  configuration containing only A;
- deletion-only update removes B while preserving A bytes/evidence;
- mixed update replaces A while removing B;
- all behavior is observed through the released CLI;
- no real repository generated branch is mutated.

## Execution order

1. Pin exact released tool 0.14.2.
2. Extend `publish_case` with removed-item main-update acceptance.
3. Run the complete external suite.
4. Merge only after every job is green.
5. Only then update Forge to exact tool 0.14.2 and retry its durable main
   cleanup.
6. Continue Forge Pages only after the stale aggregate is gone.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #56 Accept tool.cad.ci 0.14.2 removed-item durable main cleanup | now | Required released-stack proof before Forge can consume the generic cleanup fix. |

## Boundary

This repository observes released behavior only. Removed-item membership,
ownership and deletion remain library/tool behavior, never test helper logic.
