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
Set-ExecutionPolicy Unrestricted -Scope Process
python3 -m venv .venv\
.\.venv\Scripts\activate
poetry install --no-root
```

