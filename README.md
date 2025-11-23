# audio_converter
A simple python project to carry audio files conversion using ffmpeg


## Setup

ffmpeg must be installed beforehand

### Virtual env

#### Linux
```bash
python3 -m venv .venv/
source .venv/bin/activate
poetry install --no-root
```

#### Windows
```powershell
python -m venv .venv
Set-ExecutionPolicy Unrestricted -Scope Process
.\.venv\Scripts\activate
poetry install --no-root
```

## Scripts

### flac_to_mp3.py

Converts a library of .flac files to mp3.

Input library should follow the following file architecture:

```
library
    ├── artist_1
    │   ├── album_1
    │   │   ├── track_1
    │   │   ├── track_2
    │   │   └── ...
    │   └── album_2
    │       └── ...
    └── artist_2
        └── ...`
```
Output library will mirror the same file architecture.

Use the following command for more help on usage instructions.
```
python scripts/flac_to_mp3.py -h
```