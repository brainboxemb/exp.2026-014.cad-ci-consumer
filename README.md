# exp.2026-014.cad-ci-consumer

Synthetic consumer used to prove `tool.cad.ci` outside the tool repository.

The repository deliberately contains no SolidCraft logic. It tests only repository layout, affected selection, dependencies, output reuse, and partial reruns.

`dependencies.repos` pins the exact released `tool.cad.ci` commit. `scripts/bootstrap.py` checks that revision out under `ext/cad-ci`. Local runs and GitHub Actions use that same checkout.

## Run

```text
python scripts/bootstrap.py
python -m pip install -e ext/cad-ci
python tests/consumer_check.py
```

The synthetic repository contains:

```text
tests/unit/            library tests
examples/example-a/    integration example
qualification/item-a/  qualification item
qualification/item-b/  second qualification item
```

The consumer check proves that a change to `item-a` does not select `item-b`, while a shared library change reaches both dependants.
