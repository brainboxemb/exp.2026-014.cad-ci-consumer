# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released `tool.cad.ci 0.15.0` is available at exact commit
`9f37be0af5c4076f676b6407857c5905e11a47d6`.

That tool pins released `lib.py.cad.ci 0.8.4` at
`4e033fd17e911b3feb92b1a34433b884ca788ab6` and adds the root same-runner composite action required by Forge
#558.

## Current goal

Complete #58 by externally accepting the released 0.15.0 composite action
before Forge adopts it.

## Required proof

- exact released 0.15.0 revision is pinned everywhere;
- every existing CLI/reusable-workflow black-box case remains green;
- a real external job consumes `brainboxemb/tool.cad.ci@9f37be0af5c4076f676b6407857c5905e11a47d6`;
- the action executes the real `workflow_case`;
- no second checkout/setup/install occurs after the action;
- the next step imports `cad_ci_tool` from `CAD_CI_TOOL_ROOT`;
- the next step imports `cad_ci` from `CAD_CI_LIB_ROOT`;
- action output reports exact library revision `4e033fd17e911b3feb92b1a34433b884ca788ab6`;
- a real `python -m cad_ci_tool plan` succeeds on that same runner;
- action-produced build output and evidence remain available;
- no generic behavior is implemented in this repository.

## Execution order

1. [#58] Pin exact released tool.cad.ci 0.15.0.
2. [#58] Add the same-runner black-box job.
3. Run the complete external suite.
4. Merge only after every job is green.
5. Close #58 after the green merge.
6. Only then migrate Forge #558 to exact tool.cad.ci 0.15.0.

## Open issue assessment — 2026-11-21

| Issue | Status | Assessment |
| --- | --- | --- |
| #58 Accept tool.cad.ci 0.15.0 same-runner composite action | now | Required external proof before Forge removes its artifact and extra-runner main publication path. |

## Boundary

This repository observes released behavior only. Bootstrap, selection, SCons
execution, durable-store and publication behavior remain released tool/library
behavior, never test helper logic.
