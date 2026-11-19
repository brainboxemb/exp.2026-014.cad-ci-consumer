# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current goal

Complete #28: externally test released `tool.cad.ci` 0.9.0 at exact commit
`c2db9e6b6553052df12d2498e9436ba7be056fe6`, including root
`cad-ci.yml:variables`.

## Execution order

1. Pin exact tool 0.9.0 in direct bootstrap and reusable workflow use.
2. Make the existing workflow case declare a repository variable with the same
   name as a caller environment value.
3. Prove the repository value reaches the consumer command and wins.
4. Run the complete existing external test suite.
5. Merge only after green PR CI.
6. Only after green main may Forge/CAD adopt this tool release.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #28 Externally test tool.cad.ci 0.9.0 repository variables | now | Active update. Prove the exact released stack and full suite before consumer adoption. |

No other open repository issues exist at this point in time.
