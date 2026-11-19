# tool.cad.ci.test

Permanent end-to-end acceptance tests for the released `lib.py.cad.ci` +
`tool.cad.ci` stack.

This repository contains no SolidCraft, Forge or real CAD behaviour. It builds
small representative consumer repositories that prove the generic CI contract
before Forge or CAD is allowed to migrate to a new release.

`dependencies.repos` pins one exact `tool.cad.ci` commit.
`scripts/bootstrap.py` checks that revision out under `ext/cad-ci`. Local
runs and GitHub Actions use that same checkout.

## Test cases

The repository is moving to independent top-level cases:

```text
simple_case1/
more_complex_case2/
dependency_case/
partial_rerun_case/
publish_case/
timeout_case/
external_error_case/
```

Each case owns its own small `cad-ci.yml` and item tree. A case should prove
one coherent part of the CI contract so a failure immediately points at the
broken behaviour.

### simple_case1

Proves:
- one item with ordered steps;
- declared output;
- successful complete run;
- second unchanged run reuses the result.

### more_complex_case2

Proves:
- several items;
- multiple steps;
- changed-file selection;
- only affected work runs.

### dependency_case

Proves:
- dependency ordering;
- dependency changes select dependants;
- direct-only fan-in does not widen ordinary changes;
- explicit fan-in selection expands its dependencies.

### partial_rerun_case

Proves:
- exact `--step`;
- `--from`;
- `--until`;
- stale earlier state is rejected;
- partial runs do not write complete item state.

### publish_case

Proves:
- complete `build/main`;
- sparse `build/pr/<number>`;
- PR overlay resolution;
- main update of selected paths only;
- stable Pages plus PR preview;
- one-PR cleanup;
- stale-source refusal;
- retry of an actual generated-branch race.

### timeout_case

Proves:
- repository default timeout;
- step override;
- actual process termination;
- timeout stored separately from command exit failure;
- timed-out output is never reusable.

### external_error_case

Proves:
- external resource present;
- external resource explicitly absent;
- lookup/auth/network failure;
- only explicit absence may trigger creation;
- lookup errors and timeouts are never treated as "missing".

## Rules

- Cases stay small and readable.
- Cases do not contain domain behaviour.
- Generic implementation is never developed here.
- This repository consumes one exact released/pinned tool revision.
- Forge and CAD migrate only after all required cases pass.
