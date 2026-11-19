# External CAD-CI test design

`tool.cad.ci.test` is an external consumer of one exact released
`tool.cad.ci` revision. It does not implement CAD-CI behavior.

## Release identity

`dependencies.repos` pins the exact tool commit used by direct CLI cases.
The GitHub workflow calls the reusable workflow from that same exact commit.
The tool itself pins one exact released `lib.py.cad.ci` revision.

This gives one unambiguous tool/library stack for every test run.

## Test cases

Each top-level case is a small synthetic consumer repository. Cases exercise
public behavior only through the released CLI or reusable workflow.

The root `workflow_case` specifically tests the reusable workflow boundary.
For repository-variable support it supplies one caller environment value and
declares a different value with the same name in root `cad-ci.yml`. The
consumer command must observe the repository value.

This verifies the public precedence without copying variable parsing or merge
logic into this repository.

## Failure boundary

If a case exposes missing generic behavior, implementation returns to
`lib.py.cad.ci` or `tool.cad.ci`. This repository may add a failing example,
but not a local workaround.


## GHCR authentication acceptance

The root `workflow_case` remains the black-box reusable-workflow consumer.

Its command runs inside the released workflow after generic setup and checks:

```text
~/.docker/config.json
  -> auths
     -> ghcr.io exists
```

The check does not inspect the authentication value. Presence is sufficient to
prove that the released workflow executed Docker login before invoking
`cad-ci run`.

The caller workflow grants `packages: read` and calls
`reusable-ci.yml` at the same exact commit stored in `dependencies.repos`.

The test intentionally does not pull a real CAD/domain image. Package
availability and image selection are consumer concerns; this repository proves
only the generic authenticated-runner contract.
