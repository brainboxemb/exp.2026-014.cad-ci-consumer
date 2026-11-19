# Repository instructions

## Purpose

`tool.cad.ci.test` is the permanent black-box acceptance repository for one
exact released `tool.cad.ci` + `lib.py.cad.ci` stack.

Keep it synthetic and domain-neutral. Do not add Forge, SolidCraft or real CAD
behaviour.

## Released-stack rule

The repository consumes only the exact tool commit in `dependencies.repos`.
That tool must itself pin one exact released library commit.

Never follow moving `main`.

Current accepted structure:

- `simple_case1`
- `more_complex_case2`
- `dependency_case`
- `partial_rerun_case`
- `directory_output_case`
- `timeout_case`
- `publish_case`
- `workflow_case`

Each case owns a small `cad-ci.yml`, source files and `check.py`. A failure
must clearly identify the contract that broke.

## Development boundary

Do not develop generic CI behaviour here.

The sequence is:

1. define/design generic behaviour in `lib.py.cad.ci`;
2. implement, test and release the library;
3. pin that release in `tool.cad.ci`;
4. expose only the CLI adapter, test it and release the tool;
5. pin that exact tool release here;
6. prove the released stack with these cases;
7. only then migrate Forge or CAD.

If a case finds a generic gap, return to the library/tool. Do not add a local
workaround.

## Case helpers

`tests/support.py` may only provide process/file helpers such as:
- invoking the exact bootstrapped tool;
- copying a case to disposable output;
- deleting local SCons state for fresh-runner tests;
- reading JSON.

Do not put planner, SCons, cache, publication or domain decisions in the helper.

## Publication case

`publish_case` may use the real GitHub event and repository remote because its
purpose is to verify generated `build` and `gh-pages` branches.

It must use public `.cad-ci` evidence, never old custom fingerprint/state
files.

Source freshness failures, generated-branch publication and provenance are
tested through the released tool, not reimplemented in the case.

## Workflow

The workflow proves both public consumption paths:
- direct CLI cases use the exact commit in `dependencies.repos`;
- `workflow_case` calls the single high-level `reusable-ci.yml` workflow from
  the same released commit using a cross-repository `uses:` reference.

Do not rebuild plan/run/cache orchestration in this repository. The caller may
provide domain-neutral inputs and inspect generic build artifacts, but generic
selection/execution semantics stay in the released tool/library stack.

## Code and language

Use short literal engineering language and explanatory docstrings/comments for
non-obvious checks.

One logical acceptance update uses one issue, one branch and one pull request.
