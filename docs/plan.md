# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released `tool.cad.ci` 0.13.3 is available at exact commit
`bbdd473638d64e01acab69722092b2a12f99b84d`.

That tool pins released `lib.py.cad.ci` 0.8.3 at exact commit
`e8e951ed7e50c4fa754cc158729faf2927cccb31`.

The previous 0.13.2 stack already passed nested durable publication acceptance.
The remaining change to accept is operator execution logging.

## Current goal

Complete #50 by black-box accepting streamed concise execution logging.

## Required proof

- exact released tool 0.13.3 is pinned in dependency and workflow calls;
- a slow consumer exposes an early flushed line before it exits;
- output contains `CAD CI run: <item>:<step>`;
- output does not contain `_execute_bundle(` or source-list dumps;
- final CAD-CI summary remains present;
- all previous acceptance cases remain green.

## Execution order

1. Pin exact released tool 0.13.3.
2. Add one independent `logging_case`.
3. Add the case to the complete acceptance workflow.
4. Run the complete external suite.
5. Merge only after all jobs are green.
6. Only then update Forge to exact tool 0.13.3 and inspect a real Forge log.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #50 Accept tool.cad.ci 0.13.3 streamed execution logging | now | Final released-stack proof required before Forge adoption. |

## Boundary

This repository observes released logging behavior. It does not implement SCons
execution or logging mechanics.
