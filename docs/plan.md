# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released `tool.cad.ci` 0.13.2 is available at exact commit
`8d4c990cb22b794e268d361f09bc2757d15e1c94`.

That tool pins released `lib.py.cad.ci` 0.8.2 at exact commit
`d645b65281064f69f175bb645c6c956f72f3b446`.

The previous 0.13.1 stack already passed fresh cacheless Git-diff selection,
nested item configuration and parent-relative shared-input acceptance.

The first real Forge pilot then exposed a durable build-store collision between
a parent item and its nested child. 0.8.2/0.13.2 contains the generic fix.

## Current goal

Complete #48 by black-box accepting nested durable publication.

Synthetic item layout:

```text
items/model
items/model/reference
```

The test uses only the released CLI and verifies exact output/evidence ownership.

## Required proof

- full run produces parent and child complete evidence;
- `build prepare-main` succeeds with both nested items;
- `build prepare-pr --items parent child` succeeds without directory collision;
- child-only PR overlay contains no parent output/evidence;
- parent-only `update-main` preserves child output/evidence byte-for-byte;
- child-only `update-main` preserves parent output/evidence byte-for-byte;
- new durable rows expose declared `outputs` ownership metadata;
- all previous acceptance cases remain green.

## Execution order

1. Pin exact released tool 0.13.2 in dependency and workflow calls.
2. Add one independent `nested_publish_case`.
3. Add the case to the complete acceptance workflow.
4. Run the complete external suite.
5. Merge only after all jobs are green.
6. Only then resume Forge PR #499 with exact tool 0.13.2.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #48 Accept tool.cad.ci 0.13.2 nested durable publication | now | Final generic acceptance required to unblock the real Forge nested reference pilot. |

## Boundary

This repository observes the released stack. It does not implement durable
ownership, selection, SCons behavior or publication mechanics.
