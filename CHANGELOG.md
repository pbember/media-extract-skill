# Changelog

## 2026-10-03

- Pin actions/checkout, actions/setup-python to verified v7 commit SHAs. Cancel obsolete runs for the same pull request or branch.

## Unreleased

- Add `--device {auto,cuda,cpu}` and `--compute-type` to the transcription
  helper. An explicit device disables the CPU fallback. Output JSON is unchanged.
- Document `deno` as a yt-dlp prerequisite for YouTube. Correct the README
  claim that network calls are disabled during inference.

- Extend CUDA fallback to transcription and lazy segment generation. Restart
  once on CPU INT8 and discard partial GPU results before emitting JSON.
- Add entry-point regressions for CPU and GPU success, CUDA failures at each
  inference stage, and CPU failure without partial JSON.
- Document fallback behavior and the limits of automated inference tests.
- Add a documentation gate to CI. It refreshes the document index and checks
  local inline Markdown file links without fetching external URLs.
