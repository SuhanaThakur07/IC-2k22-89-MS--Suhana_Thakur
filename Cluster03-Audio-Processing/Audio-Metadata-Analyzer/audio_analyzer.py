"""
audio_analyzer.py
------------------
Cluster 03: Audio Processing

Extracts and reports audio file metadata:
    - File info: name, size, format, duration
    - Technical info: channels, sampling rate, bit depth, bit rate, codec
    - Metadata tags (title, artist, album) where available

Supported formats: WAV, MP3, FLAC, OGG, M4A

Usage:
    python audio_analyzer.py <path-to-audio>
"""

import os
import sys
import wave

try:
    import mutagen
except ImportError:
    mutagen = None

SUPPORTED_FORMATS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}

CODEC_NAMES = {
    ".wav": "PCM",
    ".mp3": "MP3",
    ".flac": "FLAC",
    ".ogg": "Vorbis",
    ".m4a": "AAC",
}


def _format_size(size_bytes):
    size = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def _format_duration(seconds):
    """MM:SS.ss format, e.g. 00:03.00"""
    if seconds is None:
        return "N/A"
    minutes = int(seconds // 60)
    secs = seconds - (minutes * 60)
    return f"{minutes:02d}:{secs:05.2f}"


def _analyze_wav(file_path):
    with wave.open(file_path, "rb") as wf:
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()   # bytes per sample
        framerate = wf.getframerate()
        n_frames = wf.getnframes()

    bit_depth = sample_width * 8
    duration = n_frames / float(framerate) if framerate else 0
    # PCM bit rate = channels * bit_depth * sample_rate
    bit_rate_kbps = (channels * bit_depth * framerate) / 1000.0

    return {
        "duration": duration,
        "channels": channels,
        "sampling_rate": framerate,
        "bit_depth": bit_depth,
        "bit_rate": bit_rate_kbps,
        "tags": {"title": "N/A", "artist": "N/A", "album": "N/A"},
    }


def _analyze_compressed(file_path):
    if mutagen is None:
        raise RuntimeError("mutagen is required to read this format. Install with: pip install mutagen")

    audio = mutagen.File(file_path, easy=True)
    if audio is None:
        raise ValueError("Could not parse audio file (unsupported or corrupt).")

    info = audio.info
    duration = getattr(info, "length", None)
    channels = getattr(info, "channels", "N/A")
    sample_rate = getattr(info, "sample_rate", "N/A")
    bitrate = getattr(info, "bitrate", None)
    bit_rate_kbps = bitrate / 1000.0 if bitrate else "N/A"

    tags = audio.tags or {}

    def tag(key, default="N/A"):
        val = tags.get(key)
        if isinstance(val, list):
            return val[0] if val else default
        return val if val else default

    return {
        "duration": duration,
        "channels": channels,
        "sampling_rate": sample_rate,
        "bit_depth": "N/A",   # not applicable to lossy/compressed formats
        "bit_rate": bit_rate_kbps,
        "tags": {
            "title": str(tag("title")),
            "artist": str(tag("artist")),
            "album": str(tag("album")),
        },
    }


def analyze_audio(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported audio format '{ext}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_FORMATS))}"
        )

    file_name = os.path.basename(file_path)
    file_size = _format_size(os.path.getsize(file_path))

    if ext == ".wav":
        data = _analyze_wav(file_path)
    else:
        data = _analyze_compressed(file_path)

    bit_rate = data["bit_rate"]
    bit_rate_str = f"{bit_rate:.2f} kbps" if isinstance(bit_rate, (int, float)) else "N/A"
    bit_depth = data["bit_depth"]
    bit_depth_str = f"{bit_depth} bits" if isinstance(bit_depth, int) else "N/A"

    return {
        "File Name": file_name,
        "File Size": file_size,
        "Format": ext.lstrip(".").upper(),
        "Duration": _format_duration(data["duration"]),
        "Channels": data["channels"],
        "Sampling Rate": f"{data['sampling_rate']} Hz" if data["sampling_rate"] != "N/A" else "N/A",
        "Bit Depth": bit_depth_str,
        "Bit Rate": bit_rate_str,
        "Codec": CODEC_NAMES.get(ext, "N/A"),
        "Tags": data["tags"],
    }


def format_report(report):
    lines = []
    lines.append("=" * 42)
    lines.append("AUDIO METADATA REPORT".center(42))
    lines.append("=" * 42)
    lines.append("")
    lines.append(f"File Name        : {report['File Name']}")
    lines.append(f"Format           : {report['Format']}")
    lines.append(f"Duration         : {report['Duration']}")
    lines.append("")
    lines.append("AUDIO")
    lines.append("-" * 42)
    lines.append(f"Channels         : {report['Channels']}")
    lines.append(f"Sampling Rate    : {report['Sampling Rate']}")
    lines.append(f"Bit Depth        : {report['Bit Depth']}")
    lines.append(f"Bit Rate         : {report['Bit Rate']}")
    lines.append(f"Codec            : {report['Codec']}")

    tags = report["Tags"]
    if any(v != "N/A" for v in tags.values()):
        lines.append("")
        lines.append("METADATA")
        lines.append("-" * 42)
        lines.append(f"Title            : {tags['title']}")
        lines.append(f"Artist           : {tags['artist']}")
        lines.append(f"Album            : {tags['album']}")

    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print("Usage: python audio_analyzer.py <path-to-audio>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        report = analyze_audio(file_path)
        print(format_report(report))
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()