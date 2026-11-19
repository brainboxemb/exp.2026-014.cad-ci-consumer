# External CAD-CI test requirements

## Exact released stack

- Every test uses one exact released `tool.cad.ci` commit.
- The reusable workflow and direct bootstrap must use the same tool commit.
- Moving branches or unreleased tool revisions are not accepted.

## Public behavior

The repository must test the released stack from outside its implementation.

The suite covers:
- normal build/current behavior;
- changed-item selection;
- dependencies and fan-out;
- partial runs;
- directory output and SCons CacheDir behavior;
- timeout/failure behavior;
- durable build and Pages publication;
- high-level reusable workflow execution and output handoff;
- reusable-workflow authentication to GitHub Container Registry.

For repository variables:
- root `cad-ci.yml:variables` must reach the consumer command;
- when the caller supplies the same non-secret environment name, the repository
  value must override it;
- CAD-CI implementation details are not reproduced in the test repository.

## Completion

A tool release is externally tested only when the complete suite is green on
the exact pinned release. Forge/CAD must not adopt the release before that.


## GHCR workflow authentication

The external reusable-workflow case must prove released tool 0.10.0 prepares
Docker authentication before the consumer CAD-CI command runs.

Acceptance rules:

- the caller grants `packages: read`;
- the real consumer command checks the runner's Docker configuration;
- `ghcr.io` must have an authentication entry;
- the test checks only presence of that entry;
- the credential value must not be printed, decoded, copied into build output or
  exposed as consumer environment;
- the test does not name or pull a Forge/SolidCraft image.

This proves generic workflow credential setup without adding domain behavior to
the acceptance repository.
