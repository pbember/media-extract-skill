#!/usr/bin/env python3
"""Transcribe a local media file with a cached Faster Whisper model."""
import argparse
import json
import sys
from pathlib import Path

DEFAULT_COMPUTE = {"cuda": "float16", "cpu": "int8"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media", type=Path)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--language", help="Language code; omit for detection")
    parser.add_argument(
        "--device", choices=("auto", "cuda", "cpu"), default="auto",
        help="auto tries CUDA, then falls back to CPU (default: auto)",
    )
    parser.add_argument(
        "--compute-type",
        help="CTranslate2 compute type for the selected device; "
        "default float16 on CUDA, int8 on CPU",
    )
    args = parser.parse_args()
    if not args.media.is_file():
        parser.error("media must be an existing local file")
    if not args.model.is_dir() or not (args.model / "model.bin").is_file():
        parser.error("model must be a cached model directory containing model.bin")

    import ctranslate2
    from faster_whisper import WhisperModel

    def transcribe(device, compute_type):
        model = WhisperModel(
            str(args.model.resolve()), device=device, compute_type=compute_type,
            local_files_only=True,
        )
        segments, info = model.transcribe(
            str(args.media.resolve()), language=args.language,
            condition_on_previous_text=False, vad_filter=True,
        )
        return {
            "method": "local-asr",
            "language": info.language,
            "segments": [
                {"start": segment.start, "end": segment.end, "text": segment.text.strip()}
                for segment in segments
            ],
        }

    device = args.device
    if device == "auto":
        device = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
    try:
        result = transcribe(device, args.compute_type or DEFAULT_COMPUTE[device])
    except Exception as exc:
        if args.device != "auto" or device != "cuda":
            raise
        print(f"warning: CUDA transcription failed ({exc}); falling back to CPU", file=sys.stderr)
        result = transcribe("cpu", DEFAULT_COMPUTE["cpu"])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
