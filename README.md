# exp.2026-014.cad-ci-consumer

Synthetic consumer used to prove `tool.cad.ci` outside the tool repository.

The repository deliberately contains no SolidCraft logic. It tests repository layout, affected selection, dependencies, output reuse, partial reruns, durable build output and Pages publication.

`dependencies.repos` pins one exact `tool.cad.ci` commit. `scripts/bootstrap.py` checks that revision out under `ext/cad-ci`. Local runs and GitHub Actions use that same checkout.

## Repository shape

```text
tests/unit/            library tests
examples/example-a/    integration example
qualification/item-a/  qualification item
qualification/item-b/  second qualification item
site/                   synthetic Pages consumer
```

## Runner checks

```text
python scripts/bootstrap.py
python -m pip install -e ext/cad-ci
python tests/consumer_check.py
```

The runner check proves:

- a change to `item-a` does not select `item-b`;
- a shared library change reaches both dependants;
- a full run succeeds;
- unchanged output is reused;
- one exact step can be rerun without rebuilding earlier steps.

## Publication checks

GitHub Actions also runs `tests/publication_check.py`.

On a pull request it publishes:

```text
build/pr/<number>/qualification/item-a/...
gh-pages/previews/pr-<number>/...
```

On `main` it publishes:

```text
build/main/<all item source paths>/...
gh-pages/
```

The test reads those generated branches back after publication and verifies the stored item state and `provenance.json`.

## Directory output proof

`qualification/item-a` has a final `package` step that declares the complete
`results/` directory as its output. CI changes a nested file after a successful
run and verifies that `tool.cad.ci` reruns only `package`; earlier current
steps are reused.
