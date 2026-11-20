# tool.cad.ci.test

Permanent black-box acceptance repository for the released generic CAD CI stack.

This repository currently pins:

- `tool.cad.ci` **0.13.0** at
  `360997f8de380a930a3ba3fcc7078bdc6f798c32`;
- that tool pins `lib.py.cad.ci` **0.8.0** at
  `e2056c0d5ac361f0d021e58e55025e02c5688acf`.

No Forge, SolidCraft or real CAD behaviour belongs here. Each top-level case is
a small independent consumer repository that exercises the released tool from
the outside.

## Cases

```text
simple_case1/
more_complex_case2/
fresh_runner_case/
nested_item_case/
dependency_case/
partial_rerun_case/
process_case/
directory_output_case/
timeout_case/
publish_case/
workflow_case/
```

`simple_case1` proves cold build, unchanged CURRENT results, verify-only
invalidation and step-input membership changes.

`more_complex_case2` proves coarse Git changed-item selection separately from
SCons target freshness.

`fresh_runner_case` proves the hosted-runner path against exact Git base/head
revisions from a new clone with no build output or SCons cache: changing only
item A executes only A and leaves independent sibling B untouched.

`nested_item_case` proves root item templates, item-root-relative watch/input
paths and path-derived nested IDs together. It changes one nested sibling in a
fresh Git clone and verifies only that sibling is planned and built.

`dependency_case` proves cumulative dependency output, fan-out and
`affected: direct` summary behaviour.

`partial_rerun_case` proves the released meanings of exact `--step`,
`--until` and `--from`, including complete-item evidence after partial runs.

`process_case` proves omitted and explicit `process: true` items participate in
normal full planning/execution, while `process: false` is excluded and rejects
explicit execution.

`directory_output_case` proves complete directory output, empty directories,
local repair and fresh-runner CacheDir restore.

`timeout_case` distinguishes repository-default timeout, per-step timeout
override and ordinary command failure.

`publish_case` proves complete main output, sparse PR output, resolved views,
real generated `build` branch publication, Pages stable/preview publication
and source/build provenance.

`workflow_case` is the root consumer used by GitHub itself. It proves the
released high-level `reusable-ci.yml` workflow from another repository. The
caller supplies `ACCEPTANCE_MARKER=reusable-workflow`, while root
`cad-ci.yml` declares `ACCEPTANCE_MARKER=repository-config`. The consumer
must observe the repository value, proving root repository variables reach the
command and override the inherited caller value.

The same real consumer command also checks that Docker already contains a
`ghcr.io` authentication entry. It checks only the registry-key presence and
never reads, decodes or writes the credential value. This proves the released reusable workflow performs generic GHCR login before
consumer CAD-CI commands.

The downstream job also verifies generated output, item evidence and step
evidence with public `output_state` terminology.

## How it runs

`dependencies.repos` stores one exact tool commit for the CLI acceptance cases.
`scripts/bootstrap.py` checks that commit out under `ext/cad-ci`.
The workflow calls only the high-level `reusable-ci.yml` from that exact
released commit. The high-level call uploads its generated `build/` tree for a
downstream acceptance job; the consumer does not rebuild generic plan/run orchestration locally.

Most cases copy their immutable template to `output/cases/<name>` before
mutating inputs. The publication case runs against its own source tree because
it also verifies the real GitHub event source SHA and generated branches.

## Boundary

If a case exposes missing generic behaviour, the implementation belongs in
`lib.py.cad.ci` first, followed by a released `tool.cad.ci`. Do not patch
around missing generic behaviour in this repository.

External package/image lookup is not a public `tool.cad.ci` command.
The Forge GHCR image-existence problem is therefore not implemented or faked in
this acceptance repository.

Forge and CAD may update their tool pin only after this exact released stack is
green here.
