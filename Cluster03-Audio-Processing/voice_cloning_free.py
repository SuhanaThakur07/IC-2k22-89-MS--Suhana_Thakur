"""
voice_cloning_free.py
----------------------
Free, local voice cloning using Coqui XTTS-v2 (open-source, no API key,
no paid account, runs entirely on your own machine).

How it works:
    1. Give it a short sample of someone's voice (6-30 seconds is enough).
    2. Give it any text.
    3. It generates new speech reading that text, in the sampled voice.

Setup (one-time):
    pip install coqui-tts torch torchaudio torchcodec

Usage:
    python voice_cloning_free.py
"""

import os
from TTS.api import TTS

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"


def clone_voice_and_speak(sample_audio_path, text, output_path, language="en"):
    """
    Loads the XTTS-v2 model and generates speech in the voice from
    sample_audio_path, saying `text`, saved to output_path.
    """
    print("\n[1/2] Loading XTTS-v2 model (first run downloads ~2GB, then it's cached)...")
    tts = TTS(MODEL_NAME, progress_bar=True, gpu=False)

    print("\n[2/2] Generating cloned speech...")
    tts.tts_to_file(
        text=text,
        speaker_wav=sample_audio_path,
        language=language,
        file_path=output_path,
    )

    print(f"\nDone! Cloned speech saved to: {output_path}")


def main():
    print("=" * 55)
    print("FREE LOCAL VOICE CLONING (Coqui XTTS-v2)")
    print("=" * 55)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_audio = os.path.join(script_dir, "voice_sample.wav")
    output_audio = os.path.join(script_dir, "cloned_voice_output.wav")

    if not os.path.exists(sample_audio):
        print(f"\nError: Voice sample not found!")
        print(f"Please place a file named 'voice_sample.wav' "
              f"(6-30 seconds, clear speech, one speaker) in this folder:")
        print(script_dir)
        return

    text = input("\nEnter the text you want the cloned voice to speak:\n> ").strip()
    if not text:
        print("Text is required! Exiting...")
        return

    clone_voice_and_speak(sample_audio, text, output_audio)


if __name__ == "__main__":
    main()