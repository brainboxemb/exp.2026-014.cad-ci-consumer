# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

The repository is updating to released `tool.cad.ci` 0.8.0 at
`5e0567346da9136b2a91d7f8b375e653f923354b`.

## Current goal

Externally prove the exact 0.8.0 release, including the new contract that the
released reusable workflow does not create persistent GitHub Actions cache
transport.

## Next execution order

1. Pin exact 0.8.0 commit in `dependencies.repos` and the reusable workflow.
2. Inspect the released `reusable-run.yml` and reject persistent cache actions.
3. Run the complete existing acceptance suite.
4. Merge only after green acceptance.
5. Only after green `main` may Forge/CAD adopt 0.8.0.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #26 Externally accept tool.cad.ci 0.8.0 without workflow cache side effects | now | Active acceptance. Prove the exact released 0.8.0 workflow and complete external suite before consumer adoption. |

Do not invent work here merely because another repository is changing. New work
belongs here only when it tests a released public `tool.cad.ci` contract.
