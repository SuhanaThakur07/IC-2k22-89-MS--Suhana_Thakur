import os
import sys
import wave
import numpy as np


def read_wav(path):
    """Read a 16-bit PCM WAV file."""

    with wave.open(path, "rb") as audio:
        channels = audio.getnchannels()
        sample_width = audio.getsampwidth()
        sample_rate = audio.getframerate()
        frame_count = audio.getnframes()
        frames = audio.readframes(frame_count)

    if sample_width != 2:
        raise ValueError("Only 16-bit WAV files are supported.")

    samples = np.frombuffer(frames, dtype=np.int16)

    if channels > 1:
        samples = samples.reshape(-1, channels)

    return samples, channels, sample_width, sample_rate


def write_wav(path, samples, channels, sample_width, sample_rate):
    """Save audio samples as a WAV file."""

    samples = np.asarray(samples, dtype=np.int16)

    with wave.open(path, "wb") as audio:
        audio.setnchannels(channels)
        audio.setsampwidth(sample_width)
        audio.setframerate(sample_rate)
        audio.writeframes(samples.tobytes())


def convert_to_mono(samples, channels):
    """Convert stereo audio to mono."""

    if channels == 1:
        return samples

    return np.mean(samples, axis=1).astype(np.int16)


def normalize_audio(samples):
    """Normalize audio volume."""

    samples = samples.astype(np.float32)

    maximum = np.max(np.abs(samples))

    if maximum == 0:
        return samples.astype(np.int16)

    normalized = (samples / maximum) * 32767

    return normalized.astype(np.int16)


def reverse_audio(samples):
    """Reverse the audio samples."""

    return samples[::-1]


def process_audio(input_path, output_dir):

    if not os.path.isfile(input_path):
        print("\nError: Input audio file does not exist.")
        return

    if not input_path.lower().endswith(".wav"):
        print("\nError: Audio processing currently supports WAV only.")
        return

    try:

        samples, channels, sample_width, sample_rate = read_wav(
            input_path
        )

        os.makedirs(output_dir, exist_ok=True)

        # 1. Stereo to Mono
        mono = convert_to_mono(samples, channels)

        write_wav(
            os.path.join(output_dir, "mono.wav"),
            mono,
            1,
            sample_width,
            sample_rate
        )

        # 2. Volume Normalization
        normalized = normalize_audio(samples)

        write_wav(
            os.path.join(output_dir, "normalized.wav"),
            normalized,
            channels,
            sample_width,
            sample_rate
        )

        # 3. Reverse Audio
        reversed_audio = reverse_audio(samples)

        write_wav(
            os.path.join(output_dir, "reversed.wav"),
            reversed_audio,
            channels,
            sample_width,
            sample_rate
        )

        print("\n" + "=" * 42)
        print("       AUDIO PROCESSING COMPLETED")
        print("=" * 42)

        print("\nGenerated outputs:")
        print(" - mono.wav")
        print(" - normalized.wav")
        print(" - reversed.wav")

        print("\nAll files saved in:")
        print(output_dir)

    except Exception as error:
        print("\nError while processing audio.")
        print(f"Details: {error}")


def main():

    if len(sys.argv) != 2:
        print("\nUsage:")
        print("python audio_processing.py <audio_path>")
        return

    input_path = sys.argv[1]

    output_dir = os.path.join(
        os.path.dirname(
            os.path.dirname(input_path)
        ),
        "output"
    )

    process_audio(input_path, output_dir)


if __name__ == "__main__":
    main()