import os
from tqdm import tqdm
from pathlib import Path
import ffmpeg
import argparse


IN_EXT = ".flac"
OUT_EXT = ".m4a"

def convertion_data(in_dir: str, out_dir: str, verbose: bool = False) -> list[dict]:
    """Scans input directory and prepares data structure for conversion
    Input directory should follow the following file structure:
    
   library
    ├── artist_1
    │   ├── album_1
    │   │   ├── track_1
    │   │   ├── track_2
    │   │   └── ...
    │   └── album_2
    │       └── ...
    └── artist_2
        └── ...

    Args:
        in_dir (str): Path to input directory.
        out_dir (str): Path to output directory.
        verbose (bool, optional): Prints warning messages. Defaults to False.

    Returns:
        list[dict]
    """
    data = []

    pbar = tqdm(os.listdir(in_dir))
    for artist in pbar:
        artist_path = os.path.join(in_dir, artist)

        for album in os.listdir(artist_path):
            pbar.set_description(f"{artist} - {album}")
            album_path = os.path.join(artist_path, album)

            for track in os.listdir(album_path):
                in_file = os.path.join(album_path, track)

                if in_file.endswith(IN_EXT):
                    out_file = os.path.join(out_dir, artist, album, track).replace(IN_EXT, OUT_EXT)
                    data.append(
                        {
                            "artist": artist,
                            "album": album,
                            "track": Path(track).stem,
                            "in_file": in_file,
                            "out_file": out_file,
                        }
                    )
                else:
                    if verbose:
                        print(f"WARNING: invalid file type: {in_file}. Ignored.")

    return data


def flac_to_aac(in_file: str, out_file: str, replace: bool = False, verbose: bool = False):
    """Converts .flac file to AAC (.m4a). Creates output partent directory if not already exists.

    Args:
        in_file (str): Absolute path to input file
        out_file (str): Absolute path to output file
        replace (bool, optional): Overwrite output file if already exists. Defaults to False.
        verbose (bool, optional): Print info messages. Defaults to False.

    Raises:
        ValueError: If input file is not .flac
    """
    if not in_file.endswith(IN_EXT):
        raise ValueError(f"Invalid file type: {in_file}")

    out_dir = Path(out_file).parent
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    def conversion(in_file, out_file):
        try:
            (
                ffmpeg
                    .input(in_file)
                    .output(
                        out_file,
                        acodec="aac",
                        audio_bitrate="192k",
                        ar="44100",
                        ac=2,
                        map="0:a:0",      # only maps audio
                    )
                    .run(quiet=True)
            )
        except ffmpeg.Error as e:
            print(f"ERROR converting {in_file}: {e.stderr.decode()}")
            if os.path.isfile(out_file):
                os.remove(out_file)

    if replace or (not replace and not os.path.isfile(out_file)):
        conversion(in_file, out_file)
    else:
        if verbose:
            print(f"INFO: {out_file} already exists. Skipping.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    parser.add_argument("-r", "--replace", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    in_dir = args.input
    out_dir = args.output
    replace = args.replace
    verbose = args.verbose

    print(f"\nScanning input directory ({in_dir}) ...")
    data = convertion_data(in_dir, out_dir, verbose)

    print("\nConverting files ...")
    pbar = tqdm(data)
    for i in pbar:
        pbar.set_description(f"{i["artist"]} - {i["album"]} - {i["track"]}")
        flac_to_aac(in_file=i["in_file"], out_file=i["out_file"], replace=replace, verbose=verbose)
