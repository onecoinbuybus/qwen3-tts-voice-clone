#!/usr/bin/env python3
"""Quick TTS script: generates and plays speech using a cloned voice.

Usage:
    speak.py <text> [--volume <float>] [--voice <name>] [--ref-text <text>]

Examples:
    speak.py "你好世界"
    speak.py "代码改好啦！" --volume 3.0
    speak.py "Hello world" --voice my_voice --ref-text "reference transcript"
"""
import argparse
import os
import sys
import shutil
import subprocess
import warnings
import re

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

def main():
    parser = argparse.ArgumentParser(description="Quick TTS with voice cloning")
    parser.add_argument("text", nargs="?", help="Text to speak")
    parser.add_argument("--volume", "-v", type=float, default=2.0,
                        help="Playback volume multiplier (default: 2.0)")
    parser.add_argument("--voice", type=str, default=None,
                        help="Voice name from voices/ directory (default: chihaya_bilibili)")
    parser.add_argument("--ref-text", type=str, default=None,
                        help="Reference transcript for voice cloning")
    args = parser.parse_args()

    if not args.text:
        parser.print_help()
        sys.exit(1)

    text = args.text

    # Reject non-Chinese text
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    if chinese_chars < len(text) * 0.3:
        print("Error: text must be primarily Chinese")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "models")
    model_path = os.path.join(models_dir, "Qwen3-TTS-12Hz-1.7B-Base-8bit")
    voices_dir = os.path.join(script_dir, "voices")

    # Resolve voice
    voice_name = args.voice or "chihaya_bilibili"
    ref_audio = os.path.join(voices_dir, f"{voice_name}.wav")
    if not os.path.exists(ref_audio):
        print(f"Error: voice '{voice_name}' not found in voices/")
        sys.exit(1)

    # Resolve reference text
    ref_text_file = os.path.join(voices_dir, f"{voice_name}.txt")
    if args.ref_text:
        ref_text = args.ref_text
    elif os.path.exists(ref_text_file):
        with open(ref_text_file, "r", encoding="utf-8") as f:
            ref_text = f.read().strip()
    else:
        ref_text = "."

    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio

    model = load_model(model_path)

    output_path = os.path.join(script_dir, "temp_speak")
    generate_audio(
        model=model,
        text=text,
        ref_audio=ref_audio,
        ref_text=ref_text,
        lang_code="zh",
        output_path=output_path,
        verbose=False,
    )

    result_file = os.path.join(output_path, "audio_000.wav")
    if os.path.exists(result_file):
        subprocess.run(["afplay", "-v", str(args.volume), result_file], check=False)
        shutil.rmtree(output_path, ignore_errors=True)

if __name__ == "__main__":
    main()
