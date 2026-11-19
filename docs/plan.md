# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

The repository currently pins released `tool.cad.ci` 0.7.1 at
`e09e86b42ee42c3171b30d031dbb84b939635ad4`, and the latest Acceptance run on
`main` is green.

There are no open repository issues at this snapshot.

## Current goal

Remain unchanged until a new `tool.cad.ci` release needs external testing.

The next expected update is after `tool.cad.ci#42` removes implicit GitHub
Actions cache behaviour.

## Next execution order

1. Wait for a released `tool.cad.ci` revision that resolves #42.
2. Pin that exact released commit in `dependencies.repos` and the reusable
   workflow call.
3. Add/keep an explicit external check that the released workflow contains no
   `actions/cache` usage and creates no CAD-CI cache transport contract.
4. Run the complete existing external test suite.
5. Only after green `main` may Forge/CAD adopt that tool release.

## Open issue assessment — 2026-11-19

No open issues.

Do not invent work here merely because another repository is changing. New work
belongs here only when it tests a released public `tool.cad.ci` contract.
