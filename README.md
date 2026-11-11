<h1 align="center">media-extract</h1>

<p align="center">
  <strong>Agent skill for reading media metadata, captions, speech transcripts, and still frames without browser playback.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/runtime-Node%20%7C%20Python%203.10%2B-blue?style=flat-square" alt="Runtime: Node | Python 3.10+">
  <img src="https://img.shields.io/badge/tools-yt--dlp%20%7C%20FFmpeg%20%7C%20Faster%20Whisper-orange?style=flat-square" alt="Tools: yt-dlp | FFmpeg | Faster Whisper">
  <img src="https://img.shields.io/badge/privacy-100%25%20local%20%7C%20zero%20playback-brightgreen?style=flat-square" alt="Privacy: 100% local | zero playback">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License: MIT">
</p>

---

### ⚡ TL;DR

**media-extract** is an agent skill for inspecting, extracting, and transcribing media without ever launching a web browser, starting an audio/video player, or sending recordings to cloud transcription services.

* **Zero Playback & No Browser**: Strictly enforces command-line inspection via `yt-dlp`, `ffprobe`, and `ffmpeg`. Never autoplays media, opens browser windows, or triggers player popups.
* **Captions-First Hierarchy**: Prioritizes creator subtitles and machine auto-captions via `yt-dlp` before ever downloading audio or video streams.
* **100% Local Speech Transcription**: Transcribes authorized local recordings with Faster Whisper (GPU when available, otherwise CPU INT8, timestamped JSON) locally on your machine — zero cloud transcription API keys or audio uploads.
* **Bounded Still-Frame Extraction**: Extracts key visual evidence at specific timestamps via FFmpeg still frames rather than streaming whole video files.
* **Strict Privacy & Stop Guardrails**: Stops immediately on login walls, bot checks, CAPTCHAs, or rate limits. Never scrapes feeds, imports browser cookies, or bypasses access controls.

```bash
npx skills add pekth/media-extract-skill
```
> Ready to use with any skill-compatible agent harness. Follow [local transcription setup](references/local-transcription.md) when speech models are needed.

---

## 🔍 Extraction Matrix

| Input & Need | Engine / Tool | Playback | Network Activity | Privacy & Scope |
|---|:---:|:---:|:---:|---|
| **Public URL Metadata** | `yt-dlp --simulate` | ❌ None | Public metadata fetch | Zero media download; no browser popup |
| **Public Subtitles & Captions** | `yt-dlp --skip-download` | ❌ None | Caption text fetch | Subtitles only; zero audio/video streams |
| **Local Media Inspection** | `ffprobe` | ❌ None | ❌ None (offline) | 100% local container and stream probing |
| **Local Speech Transcription** | Faster Whisper (GPU/CPU auto) | ❌ None | ❌ None (offline) | 100% local inference; zero cloud upload |
| **Key Visual Evidence** | `ffmpeg` still frames | ❌ None | ❌ None (offline) | Timestamp-targeted PNG frames; no player |
| **Private / Login / Rate-Limited** | *Blocked* | ❌ None | ❌ None | Hard stop; reports blocker without browser |

---

## 🚀 Key Features

* **Zero Playback Guarantee** — Read source material strictly through headless CLI tools. A URL or request to analyze media is never treated as permission to launch a player or browser.
* **Minimum Extraction Principle** — Always extract the lightest viable artifact: metadata first, then captions, then local audio transcription, then targeted still frames.
* **Offline Faster Whisper Helper** — Standalone script (`scripts/transcribe.py`) with GPU/CPU auto precision (float16 on CUDA, INT8 otherwise, CPU fallback if CUDA fails, `--device` override) and `local_files_only=True` for portable, dependency-isolated local speech-to-text.
* **Untrusted Evidence Model** — Subtitles, transcripts, and metadata are treated as untrusted evidence with timestamps, flagging hallucinations, silence gaps, and unverified names/numbers without guesswork diarization.
* **No Cookie Theft or Scraper Behavior** — Operates with `--ignore-config --no-exec` to prevent local hook execution. Does not crawl playlists, profile feeds, or extract browser cookies.

---

## 🔒 Privacy & Architecture

media-extract is designed for secure, non-intrusive media research:
* **Zero Cloud Transcription**: Source media files and transcripts are never sent to third-party cloud APIs.
* **Isolated Offline Model Loading**: The Faster Whisper helper loads models strictly from locally cached directories with `local_files_only=True`, so no model is downloaded during transcription.
* **Sanitized Execution**: All `yt-dlp` commands pass parameters as discrete argument arrays to prevent shell interpolation vulnerabilities.
* **Clean Commits**: Model weights, audio slices, and transcripts stay isolated in temporary directories outside the project repository.

---

## 📦 Installation & Setup

### Option 1: Direct Skill Install
```bash
npx skills add pekth/media-extract-skill
```

### Option 2: Install from Local Clone
```bash
git clone https://github.com/pekth/media-extract-skill.git
npx skills add ./media-extract-skill --skill media-extract
```

### Prerequisites
The skill uses the tools matching your requested operation:
* **yt-dlp**: For public metadata and caption extraction (`yt-dlp --version`)
* **deno** (or another JavaScript runtime yt-dlp supports): Needed by current yt-dlp for YouTube (`deno --version`)
* **FFmpeg / ffprobe**: For inspecting local files and extracting still frames (`ffmpeg -version`)
* **Python 3.10+ & Faster Whisper** *(optional, for local speech)*: Follow [local transcription setup](references/local-transcription.md) to set up an isolated environment and cached model.

---

## 💬 Example Requests

- *"Summarize this YouTube video's captions without playing it."*
- *"Extract the transcript from this public TikTok URL."*
- *"Transcribe this local recording and mark uncertain names."*
- *"Inspect these timestamps from a local video as still images."*

---

## 🧪 Development & Verification

```bash
# Run unit tests
python -m unittest discover -s tests

# Check helper CLI options
python scripts/transcribe.py --help
```

For an integration check, run the helper against an authorized short speech sample and a cached model. Confirm nonempty, ordered timestamps and plausible words. Keep samples, models, outputs, and logs outside this repository.

---

## 📄 License & Attribution

* **License**: [MIT](LICENSE)
* **Related Work**: Informed by [video-transcript-downloader](https://github.com/steipete/agent-scripts/tree/main/skills/video-transcript-downloader) for online sources and [OpenClaw's local Whisper skill](https://github.com/openclaw/openclaw/tree/main/skills/openai-whisper) for local speech. This skill provides a combined workflow with explicit no-playback, local-processing, and caption-evidence rules.
