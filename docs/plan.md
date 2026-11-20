# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released `tool.cad.ci` 0.13.1 is available at exact commit
`f357b70599e5b0a6cf39a25de6a70e43a04e85b1`.

That tool pins released `lib.py.cad.ci` 0.8.1 at exact commit
`ab701bf9ef46892040f4593a74b16805b7187bea`.

The previous 0.13.0 stack already passed nested template/local-path and fresh
Git-diff sibling-isolation acceptance.

## Current goal

Complete #46 by accepting safe parent-relative item paths in the existing
nested black-box consumer.

The root template will include:

```yaml
watch:
  item:
    - "**"
    - ../verification/reference_geometry.json
```

and the same parent contract in step `inputs`.

## Required proof

From exact Git revisions and fresh clones:

1. changing only `build123d/model.py` selects/builds only the build123d child;
2. changing the shared parent `verification/reference_geometry.json` selects
   and builds both nested child siblings;
3. both children can consume the parent contract during their command;
4. no previous `build/` or `.cache/cad-ci/` is required;
5. all existing acceptance cases remain green.

## Execution order

1. Pin exact released tool 0.13.1 in dependency and workflow calls.
2. Extend `nested_item_case` with the parent-owned contract path.
3. Prove child-only and parent-shared Git selections.
4. Run the complete external suite.
5. Merge only after every case is green.
6. Only then start the Forge reference migration.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #46 Accept tool.cad.ci 0.13.1 parent-relative nested inputs | now | Final generic acceptance of the real parent-contract pattern required before Forge adoption. |

## Boundary

This repository observes the exact released stack. It does not implement
configuration, path normalization, selection, SCons behavior or publication.
