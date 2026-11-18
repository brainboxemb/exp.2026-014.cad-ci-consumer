# Repository instructions

## Purpose

This repository is a synthetic consumer for `tool.cad.ci`. Keep it small and artificial. Do not add SolidCraft, Forge, or real CAD behaviour here.

## Language

Write like an engineer explaining the repository to another engineer.

- Use short, direct sentences.
- Use normal engineering words.
- Avoid academic, management, and architecture-heavy wording.
- Prefer concrete names from the files and commands.

## Code comments

Comments explain why something is needed. Do not restate simple code.

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
- one step can be rerun without rerunning earlier steps.

## Tool pin

`tool.cad.ci` is an external tool, not copied source.

- Keep its exact commit in `dependencies.repos`.
- Bootstrap it under `ext/cad-ci`.
- Local checks and GitHub Actions use the same pinned checkout.
- Never follow moving `main` in CI.
