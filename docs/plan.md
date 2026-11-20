# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

Released `tool.cad.ci` 0.12.3 is pinned at exact commit
`ad7099b4712af13067c1c42ad50e89bf6a8306dd`.

That tool pins released `lib.py.cad.ci` 0.7.1.

The released reusable workflow intentionally contains no persistent SCons cache
transport. Hosted-runner incrementality must therefore be proven through Git
changed-item selection, not assumed cross-run cache reuse.

## Current goal

Complete #42: prove the released stack on a fresh cacheless Git workspace.

The acceptance case must create two independent items, change only item A
between exact base/head commits, clone the head into a new workspace and invoke
the released CLI with those exact Git revisions.

Expected:

```text
Git diff -> A only
plan     -> A only
run      -> A built
B        -> not executed, no build output
```

## Execution order

1. Add a synthetic `fresh_runner_case`.
2. Verify the case starts with no `build/` and no `.cache/cad-ci/`.
3. Use released CLI `--base/--head`; do not pass a hand-written `--changed`.
4. Add the case to the existing complete acceptance workflow.
5. Run the entire external suite.
6. Merge only when all existing and new cases are green.
7. Only then allow the Forge reference-item migration to begin.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #42 Prove Git-selected cold execution on a fresh runner | now | Required external proof of the real hosted-runner path before Forge migration. |

## Boundary

This repository observes the released stack from outside. It does not implement
selection, caching, SCons behavior or publication.
