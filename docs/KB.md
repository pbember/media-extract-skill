# Repository knowledge

## Local transcription

[The helper](../scripts/transcribe.py) validates local media and a cached model
directory before importing ASR dependencies. It loads models with
`local_files_only=True` and returns timestamped `local-asr` JSON.

CUDA float16 is preferred when a CUDA device is detected. The helper consumes
all GPU segments inside the fallback guard. If that attempt fails, it restarts
once on CPU INT8 and discards partial GPU text. A CPU failure propagates without
JSON output. `--device cuda` or `--device cpu` disables the fallback, and
`--compute-type` overrides precision for the selected device only. See [local transcription setup](../references/local-transcription.md)
for dependencies and model preparation.

## Verification

Run `python3 -m unittest discover -s tests -v`. Inference tests execute the
helper entry point with controlled ASR adapters. They verify fallback, JSON,
and offline model-loading arguments without downloading models or reading
private media. They do not prove real CUDA availability or speech accuracy.

For real inference proof, use an authorized speech sample and a cached model
as described in [the README](../README.md#-development--verification).

## Documentation gate

After adding, removing, or renaming a Markdown document, run
`python3 scripts/documentation.py --write` to refresh the index below. Run
`python3 scripts/documentation.py --check` before delivery. The gate includes
tracked and untracked Markdown documents that Git does not ignore. It checks
local inline file links, including links to source files, without fetching
external URLs or checking heading fragments. The write mode preserves authored
knowledge and rejects malformed index markers before writing. CI runs the check
mode on pull requests. See [ADR-0001](adr/0001-documentation-gate.md).

## Document index

<!-- documentation:start -->
- `AGENTS.md`
- `CHANGELOG.md`
- `CLAUDE.md`
- `README.md`
- `SKILL.md`
- `docs/KB.md`
- `docs/adr/0001-documentation-gate.md`
- `references/local-transcription.md`
<!-- documentation:end -->

## CI workflow maintenance

- [ci.yml](../.github/workflows/ci.yml) uses full-SHA v7 pins for `actions/checkout`, `actions/setup-python`. Application language versions and explicit cache settings are preserved.
- Obsolete runs for the same pull request or branch are cancelled. Existing timeout caps are preserved.

Reviewed base: `e3092132d2002c64ba074e339d93537c4d0204ce`. Source checks do not prove runtime, deployment or device behavior.
