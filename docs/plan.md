# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released `tool.cad.ci` 0.13.0 is available at exact commit
`360997f8de380a930a3ba3fcc7078bdc6f798c32`.

That tool pins released `lib.py.cad.ci` 0.8.0 at exact commit
`e2056c0d5ac361f0d021e58e55025e02c5688acf`.

The previous released stack already passed the fresh cacheless hosted-runner
Git-diff acceptance. The new stack adds only local nested-item configuration
features in the library.

## Current goal

Complete #44 as black-box acceptance of exact tool 0.13.0.

Add one nested domain-neutral case that proves:

- root named template;
- child-local `item` watch/input paths;
- omitted nested IDs become path-derived IDs;
- exact base/head Git diff changes one sibling;
- fresh clone has no previous build/cache;
- only the changed sibling is planned and built.

## Execution order

1. Pin exact released tool commit
   `360997f8de380a930a3ba3fcc7078bdc6f798c32`.
2. Pin the same exact commit in reusable workflow calls.
3. Add `nested_item_case`.
4. Add it to the complete acceptance workflow.
5. Run the entire external suite.
6. Merge only after every existing and new case is green.
7. Only then allow one Forge model/reference pilot.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #44 Accept tool.cad.ci 0.13.0 nested local item configuration | now | Final generic acceptance required before Forge reference-item migration. |

## Boundary

This repository observes the released stack from outside. It does not implement
configuration composition, selection, SCons behavior or publication.
