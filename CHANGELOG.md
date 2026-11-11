# Changelog

## Unreleased

- Transcription helper: fall back to CPU when CUDA fails during model load or
  decoding, not only at load. Add `--device {auto,cuda,cpu}` and
  `--compute-type`. Output now includes `device` and `compute_type`.
- Use the GPU when available and skip the WAV re-encode step.
- Docs: list `deno` as a yt-dlp prerequisite for YouTube.
- Tests: stub-based tests for output shape, language passthrough and device
  selection.
