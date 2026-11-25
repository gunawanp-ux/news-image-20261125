"""Entrypoint: hand the finished front page to the grader.

The picture itself was drawn ahead of time by generate_image.py and kept
beside this file as entry.png. When the harness runs this program it only
needs the bytes in /output/entry.png, so all this does is place a copy
there, making the directory first if it is not there yet.
"""

import shutil
from pathlib import Path

HERE = Path(__file__).parent
FINISHED = HERE / "entry.png"
TARGET = Path("/output") / "entry.png"


def main():
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(FINISHED, TARGET)
    size = TARGET.stat().st_size
    assert size > 0, "copied entry image is empty"
    print(f"entry image placed at {TARGET} ({size} bytes)")


if __name__ == "__main__":
    main()
