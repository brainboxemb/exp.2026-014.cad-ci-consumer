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
- high-level reusable workflow execution and output handoff.

For repository variables:
- root `cad-ci.yml:variables` must reach the consumer command;
- when the caller supplies the same non-secret environment name, the repository
  value must override it;
- CAD-CI implementation details are not reproduced in the test repository.

## Completion

A tool release is externally tested only when the complete suite is green on
the exact pinned release. Forge/CAD must not adopt the release before that.
