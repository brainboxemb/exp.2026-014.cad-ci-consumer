# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current goal

Complete #30: externally test released `tool.cad.ci` **0.10.0** at exact
commit `c60bf64a393dff33440d22e9e9347cbbaba71c4b`.

The release adds generic GHCR authentication to the reusable CAD-CI workflow.
The external test must prove that a real consumer command runs with Docker
already authenticated to `ghcr.io`, while retaining all existing 0.9.0
acceptance behavior.

## Execution order

1. Pin the exact 0.10.0 tool commit in `dependencies.repos`.
2. Call `reusable-ci.yml` from the same exact 0.10.0 commit.
3. Grant the caller `packages: read`.
4. Extend `workflow_case` so its real CAD-CI command verifies only that
   Docker configuration contains a `ghcr.io` authentication entry.
5. Never print, decode or copy the credential value.
6. Run the complete existing external acceptance suite.
7. Merge only after green PR CI.
8. Verify green main acceptance before Forge adopts tool 0.10.0.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #30 Externally test tool.cad.ci 0.10.0 GHCR authentication | now | Required black-box proof before Forge may use the new reusable workflow for its private/shared runtime package. |

No other implementation issues are currently open in this repository.

## Boundary

This repository proves the released workflow from outside. It does not implement
registry login, CAD-CI behavior or Forge/SolidCraft behavior.
