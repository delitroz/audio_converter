import os
from tqdm import tqdm
from pathlib import Path
import ffmpeg
import argparse


IN_EXT = ".flac"
OUT_EXT = ".m4a"

def convertion_data(in_dir: str, out_dir: str):
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

    Parameters
    ----------
    in_dir : str
        Path to the input directory.
    out_dir : str
        Path to the output directory.

    Returns
    -------
    list[dict]
    """
    data = []

    for artist in os.listdir(in_dir):
        artist_path = os.path.join(in_dir, artist)

        for album in os.listdir(artist_path):
            album_path = os.path.join(artist_path, album)

            for track in os.listdir(album_path):
                in_file = os.path.join(album_path, track)

                if in_file.endswith(IN_EXT):
                    out_file = in_file.replace(in_dir, out_dir).replace(IN_EXT, OUT_EXT)
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
                    print(f"WARNING: invalid file type: {in_file}. Ignored.")

    return data


def flac_to_aac(in_file: str, out_file: str):
    """Converts .flac file to AAC (.m4a). Creates output partent directory if not already exists.

    Parameters
    ----------
    in_file : str
        absolute path to input file
    out_file : str
        absolute path to output file

    Raises
    ------
    ValueError
        If input file is not .flac
    """
    if not in_file.endswith(IN_EXT):
        raise ValueError(f"Invalid file type: {in_file}")

    out_dir = Path(out_file).parent
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    if not os.path.isfile(out_file):
        try:
            ffmpeg.input(in_file).output(out_file, acodec='aac').run(quiet=True)
        except ffmpeg.Error as e:
            print(f"An error occurred: {e}")


def main(in_dir, out_dir):
    print(f"\n\nScanning input library ({in_dir})...")
    data = convertion_data(in_dir, out_dir)

    print("\n\nConverting files...")
    pbar = tqdm(data)
    for i in pbar:
        pbar.set_description(f"{i['artist']} - {i['album']} - {i['track']}")
        flac_to_aac(i["in_file"], i["out_file"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")

    args = parser.parse_args()
    in_dir = args.input
    out_dir = args.output

    main(in_dir, out_dir)
