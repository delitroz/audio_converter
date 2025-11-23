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

