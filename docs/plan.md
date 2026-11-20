# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current goal

Complete #32: externally test released `tool.cad.ci 0.11.0` at exact commit
`96d4c9d6076b7452933c048ace65cf2b0a159d64`.

That tool pins `lib.py.cad.ci 0.6.0` and exposes item-level `process`
participation through the existing thin CLI/workflow stack.

## Execution order

1. Pin exact tool 0.11.0 commit in `dependencies.repos`.
2. Keep direct CLI and reusable workflow consumption on that same exact commit.
3. Add one synthetic `process_case` that proves:
   - normal processed items execute;
   - `process: false` items are absent from a full plan/run;
   - explicit execution of a non-processed item fails clearly.
4. Run the complete existing external acceptance suite.
5. Merge only after green PR CI.
6. Verify green main acceptance before Forge adopts tool 0.11.0.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #32 Externally test tool.cad.ci 0.11.0 process selection | now | Required released-stack proof before Forge may use staged item processing. |
| #34 Stop publishing an unused repository Pages site | later | Repository/CI housekeeping. Keep separate from #32 and preserve `publish_case` coverage of released Pages behavior. |

## Released state

The previous 0.10.0 GHCR acceptance work is complete. It remains part of the
regression suite but is no longer active work.

## Boundary

This repository proves released behavior from outside. It does not parse
`process`, calculate selection itself or implement CAD-CI behavior.
