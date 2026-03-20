#!/usr/bin/env python3
"""Quick TTS script: generates and plays speech using a cloned voice."""
import os
import sys
import shutil
import subprocess
import warnings
import re

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else None
    if not text:
        print("Usage: speak.py <text>")
        sys.exit(1)

    # Reject non-Chinese text
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    if chinese_chars < len(text) * 0.3:
        print("Error: text must be primarily Chinese")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "models")
    model_path = os.path.join(models_dir, "Qwen3-TTS-12Hz-1.7B-Base-8bit")
    ref_audio = os.path.join(script_dir, "voices", "reference.wav")

    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio

    model = load_model(model_path)

    output_path = os.path.join(script_dir, "temp_speak")
    generate_audio(
        model=model,
        text=text,
        ref_audio=ref_audio,
        ref_text="这里填写参考音频对应的文本内容",
        lang_code="zh",
        output_path=output_path,
        verbose=False,
    )

    result_file = os.path.join(output_path, "audio_000.wav")
    if os.path.exists(result_file):
        subprocess.run(["afplay", result_file], check=False)
        shutil.rmtree(output_path, ignore_errors=True)


if __name__ == "__main__":
    main()
