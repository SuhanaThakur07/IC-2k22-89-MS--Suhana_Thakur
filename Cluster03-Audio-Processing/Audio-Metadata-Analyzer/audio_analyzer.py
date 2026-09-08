import os
import sys
import wave
from mutagen import File


SUPPORTED_FORMATS = {
    ".wav",
    ".mp3",
    ".flac",
    ".ogg",
    ".m4a"
}


def format_size(size):
    """Convert bytes into a readable file size."""

    if size < 1024:
        return f"{size} Bytes"

    if size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"

    return f"{size / (1024 * 1024):.2f} MB"


def format_duration(seconds):
    """Convert seconds into MM:SS format."""

    minutes = int(seconds // 60)
    seconds = seconds % 60

    return f"{minutes:02d}:{seconds:05.2f}"


def analyze_wav(path):
    """Extract technical information from a WAV file."""

    with wave.open(path, "rb") as audio:
        channels = audio.getnchannels()
        sample_rate = audio.getframerate()
        bit_depth = audio.getsampwidth() * 8
        frame_count = audio.getnframes()

    duration = (
        frame_count / sample_rate
        if sample_rate > 0
        else 0
    )

    bit_rate = sample_rate * bit_depth * channels

    return {
        "channels": channels,
        "sample_rate": sample_rate,
        "bit_depth": bit_depth,
        "duration": duration,
        "bit_rate": bit_rate,
        "codec": "PCM"
    }


def analyze_audio(path):
    """Analyze an audio file and display its metadata."""

    if not os.path.isfile(path):
        print("\nError: Audio file not found.")
        return

    extension = os.path.splitext(path)[1].lower()

    if extension not in SUPPORTED_FORMATS:
        print("\nError: Unsupported audio format.")
        print("Supported: WAV, MP3, FLAC, OGG, M4A")
        return

    try:
        file_size = os.path.getsize(path)

        # WAV files can be analyzed using Python's built-in module.
        if extension == ".wav":

            info = analyze_wav(path)

            metadata = {
                "title": "Not Available",
                "artist": "Not Available",
                "album": "Not Available"
            }

        else:

            audio = File(path)

            if audio is None or audio.info is None:
                print("\nError: Unable to read audio information.")
                return

            info = {
                "channels": getattr(
                    audio.info,
                    "channels",
                    "Not Available"
                ),
                "sample_rate": getattr(
                    audio.info,
                    "sample_rate",
                    "Not Available"
                ),
                "bit_depth": "Not Available",
                "duration": getattr(
                    audio.info,
                    "length",
                    0
                ),
                "bit_rate": getattr(
                    audio.info,
                    "bitrate",
                    "Not Available"
                ),
                "codec": extension.upper().replace(".", "")
            }

            metadata = {
                "title": audio.get("TIT2", ["Not Available"])[0],
                "artist": audio.get("TPE1", ["Not Available"])[0],
                "album": audio.get("TALB", ["Not Available"])[0]
            }

        print("\n" + "=" * 42)
        print("           AUDIO METADATA REPORT")
        print("=" * 42)

        print(f"\n{'File Name':<18}: {os.path.basename(path)}")
        print(f"{'File Size':<18}: {format_size(file_size)}")
        print(f"{'Format':<18}: {extension.upper().replace('.', '')}")
        print(f"{'Duration':<18}: {format_duration(info['duration'])}")

        print("\nAUDIO")
        print("-" * 42)

        print(f"{'Channels':<18}: {info['channels']}")
        print(f"{'Sampling Rate':<18}: {info['sample_rate']} Hz")
        print(f"{'Bit Depth':<18}: {info['bit_depth']} bits")

        bitrate = info["bit_rate"]

        if isinstance(bitrate, (int, float)):
            bitrate = f"{bitrate / 1000:.2f} kbps"

        print(f"{'Bit Rate':<18}: {bitrate}")
        print(f"{'Codec':<18}: {info['codec']}")

        print("\nMETADATA")
        print("-" * 42)

        print(f"{'Title':<18}: {metadata['title']}")
        print(f"{'Artist':<18}: {metadata['artist']}")
        print(f"{'Album':<18}: {metadata['album']}")

        print("\n" + "=" * 42)

    except Exception as error:
        print("\nError while analyzing audio.")
        print(f"Details: {error}")


def main():

    if len(sys.argv) != 2:
        print("\nUsage:")
        print("python audio_analyzer.py <audio_path>")
        return

    analyze_audio(sys.argv[1])


if __name__ == "__main__":
    main()