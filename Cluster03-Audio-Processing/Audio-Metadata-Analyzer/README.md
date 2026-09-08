# Cluster 03: Audio Processing

## Problem Statement

To analyze audio files and implement basic audio processing operations using Python while extracting important technical and metadata information.

## Objectives

- Understand basic digital audio concepts.
- Extract audio file metadata.
- Determine duration, channels, sampling rate and bit depth.
- Calculate audio bit rate.
- Convert stereo audio to mono.
- Normalize audio volume.
- Reverse audio samples.
- Save processed audio as output files.

## Technologies Used

- Python 3
- NumPy
- Mutagen
- Python Wave Module

## Input

The analyzer supports:

- WAV
- MP3
- FLAC
- OGG
- M4A

Audio processing currently supports:

- WAV
- 16-bit PCM audio

Sample input:

```text
input/sample.wav

Audio Analyzer

The audio_analyzer.py program extracts:

File Information
File name
File size
Audio format
Duration
Technical Information
Number of channels
Sampling rate
Bit depth
Bit rate
Codec
Metadata

For supported tagged audio formats, the analyzer can display:

Title
Artist
Album
Audio Processing

The audio_processing.py program performs three basic operations.

1. Stereo to Mono Conversion

Converts multi-channel stereo audio into a single-channel mono signal.

2. Volume Normalization

Scales the audio samples so that the signal uses the available amplitude range more effectively.

3. Audio Reversal

Reverses the sequence of audio samples, producing a reversed version of the original audio.

Algorithm / Workflow
Start
  ↓
Read audio file
  ↓
Validate file
  ↓
Extract audio information
  ↓
Display metadata report
  ↓
Read WAV samples
  ↓
Convert stereo to mono
  ↓
Normalize audio
  ↓
Reverse audio
  ↓
Save processed files
  ↓
End
Sample Input
input/sample.wav

The sample audio is a 16-bit PCM WAV file with a 44.1 kHz sampling rate.

Sample Output

The analyzer displays information such as:

==========================================
           AUDIO METADATA REPORT
==========================================

File Name        : sample.wav
Format           : WAV
Duration         : 00:03.00

AUDIO
------------------------------------------
Channels         : 2
Sampling Rate    : 44100 Hz
Bit Depth        : 16 bits
Bit Rate         : 1411.20 kbps
Codec            : PCM

The processing program generates:

output/
├── mono.wav
├── normalized.wav
└── reversed.wav
Error Handling

The programs handle:

Missing input files
Unsupported audio formats
Invalid audio files
Unsupported WAV bit depth
Errors during audio reading or writing
Missing output directories
Performance Analysis

The implementation is lightweight and does not use machine learning or computationally expensive audio-analysis libraries.

Audio processing operates directly on WAV samples using NumPy.

Processing time primarily depends on:

Audio duration
Sampling rate
Number of channels
File size
Learning Outcomes

After completing this experiment, the following concepts were understood:

Digital audio representation
Sampling rate
Bit depth
Channels
Bit rate
Audio metadata
PCM audio
Mono conversion
Volume normalization
Audio reversal
WAV file handling
Screenshots / Output

Add screenshots showing:

Audio analyzer execution
Audio metadata report
Audio processing execution
Generated output files
References
Python Documentation
NumPy Documentation
Mutagen