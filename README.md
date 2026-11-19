# tool.cad.ci.test

Permanent black-box acceptance repository for the released generic CAD CI stack.

This repository currently pins:

- `tool.cad.ci` **0.6.1** at
  `b9a2f62c482ce85e07044fac21786ea4ea771ff2`;
- that tool pins `lib.py.cad.ci` **0.3.0** at
  `155ec24915e7b2d1b9f5306db9df84a50b53dba8`.

No Forge, SolidCraft or real CAD behaviour belongs here. Each top-level case is
a small independent consumer repository that exercises the released tool from
the outside.

## Cases

```text
simple_case1/
more_complex_case2/
dependency_case/
partial_rerun_case/
directory_output_case/
timeout_case/
publish_case/
```

`simple_case1` proves cold build, unchanged CURRENT results, verify-only
invalidation and step-input membership changes.

`more_complex_case2` proves coarse Git changed-item selection separately from
SCons target freshness.

`dependency_case` proves cumulative dependency output, fan-out and
`affected: direct` summary behaviour.

`partial_rerun_case` proves the released meanings of exact `--step`,
`--until` and `--from`, including complete-item evidence after partial runs.

`directory_output_case` proves complete directory output, empty directories,
local repair and fresh-runner CacheDir restore.

`timeout_case` distinguishes repository-default timeout, per-step timeout
override and ordinary command failure.

`publish_case` proves complete main output, sparse PR output, resolved views,
real generated `build` branch publication, Pages stable/preview publication
and source/build provenance.

`workflow_case` is the root consumer used by GitHub itself. It proves the released
cross-repository plan workflow and the high-level reusable CI workflow. The
consumer command fails unless the declared non-secret environment reaches it;
the downstream acceptance job also downloads the handed-off build artifact and
checks both `result.txt` and hidden `.cad-ci/item.json` evidence.

## How it runs

`dependencies.repos` stores one exact tool commit for the CLI acceptance cases.
`scripts/bootstrap.py` checks that commit out under `ext/cad-ci`.
The same workflow calls `reusable-plan.yml` and the high-level `reusable-ci.yml`
directly from that exact released commit. The high-level call uploads its
materialized `build/` tree for a downstream acceptance job.

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
