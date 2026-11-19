# Repository instructions

## Purpose

`tool.cad.ci.test` is the permanent end-to-end acceptance repository for the
released `lib.py.cad.ci` + `tool.cad.ci` stack.

Keep this repository synthetic and domain-neutral. Do not add SolidCraft, Forge
or real CAD behaviour here.

## Test structure

Use several independent top-level consumer cases instead of one catch-all
synthetic repository.

Expected cases include:

- `simple_case1`
- `more_complex_case2`
- `dependency_case`
- `partial_rerun_case`
- `publish_case`
- `timeout_case`
- `external_error_case`

Each case should have a small understandable `cad-ci.yml` and item tree and
prove one coherent contract.

A failure should make it obvious which generic CI behaviour broke.

## Development boundary

Do not develop generic CI behaviour in this repository.

The sequence is:

1. define the requirement in `lib.py.cad.ci`;
2. implement and unit-test it there;
3. release the library;
4. expose the released library through `tool.cad.ci`;
5. release the tool;
6. pin that exact tool release here;
7. prove the complete stack with the representative cases;
8. only then migrate Forge or CAD.

If a case reveals missing generic behaviour, return the work to the library or
tool. Do not patch around it in this repository.

## Tool pin

`tool.cad.ci` is external tooling.

- Keep its exact commit in `dependencies.repos`.
- Bootstrap it under `ext/cad-ci`.
- Local checks and GitHub Actions use the same pinned checkout.
- Never follow moving `main` in CI.

## Language and code

Use short, direct engineering language. Prefer names that say what the code
actually does.

Code must explain non-obvious flow, reuse rules, publication safety and failure
handling with concise docstrings/comments.

Keep one logical change in one branch and pull request.
