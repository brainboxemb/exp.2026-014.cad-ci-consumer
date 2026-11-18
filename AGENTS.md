# Repository instructions

## Purpose

This repository is a synthetic consumer for `tool.cad.ci`. Keep it small and artificial. Do not add SolidCraft, Forge, or real CAD behaviour here.

It exists to prove the tool itself before Forge or CAD consumes a new release.

## Language

Write like an engineer explaining the repository to another engineer.

- Use short, direct sentences.
- Use normal engineering words.
- Avoid academic, management, and architecture-heavy wording.
- Prefer concrete names from the files and commands.

## Code comments and explanations

Code should explain its important flow and safety rules.

- Give non-trivial modules/functions a short explanation.
- Explain why a publication or reuse check exists.
- Explain why one generated namespace is changed and another is preserved.
- Do not add comments that only repeat Python syntax.

## Git

Keep one logical change in one branch and pull request. Run the consumer checks before merging. Do not mix unrelated experiments into this repository.

## Test role

The repository must keep proving these cases:

- one library-test item;
- one integration item;
- two qualification items;
- a qualification change does not select its sibling;
- a shared library change reaches all dependants;
- a full run succeeds;
- a second unchanged run reuses output;
- one step can be rerun without rerunning earlier steps;
- a PR build is a sparse `build/pr/<number>` overlay;
- main build output is a complete `build/main` baseline;
- Pages previews live below `previews/pr-<number>/`;
- stable Pages and previews do not overwrite each other;
- generated branch output can be read back after the GitHub publication.

## Tool pin

`tool.cad.ci` is an external tool, not copied source.

- Keep its exact commit in `dependencies.repos`.
- Bootstrap it under `ext/cad-ci`.
- Local checks and GitHub Actions use the same pinned checkout.
- Never follow moving `main` in CI.
- During tool development this synthetic repo may temporarily pin the exact commit of an open tool PR. Replace that pin with the released commit after the release is published.
