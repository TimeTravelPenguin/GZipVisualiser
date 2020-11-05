"""
Made by: Phillip Smith --- c3322845
Contact: Phillip.E.Smith@uon.edu.au
Date: 2020/11/01

This script was made in one night,
so it is prone to bugs
"""

import gzip
from typing import List, Tuple

import numpy as np
from PIL import Image


# read file as binary input
def ReadFile(dir: str) -> bytearray:
    try:
        data = open(dir, mode="rb")
        return bytearray(data.read())
    except IOError:
        raise Exception(f"IOError: Error opening file {dir}")


# normalize colour data between 0 and 255
def BitstreamNormalizeRGB(arr: np.array) -> List[float]:
    last = arr[0]
    cnt = 0
    freq = []
    for bit in arr:
        if bit == last:
            cnt += 1
        else:
            freq.append(cnt)
            last = bit
            cnt = 0
    freq.append(cnt)

    normFreq = 255 * (arr - min(arr)) / (max(arr) - min(arr))
    normDat = []
    for c in range(len(freq)):
        for f in range(freq[c]):
            normDat.append(normFreq[c])

    print(normDat)
    return normDat


# process (r, g, b, a) data into img
def save_img(data: List[Tuple[int, int, int, int]], filename: str) -> None:
    k = len(data)
    r = 4 / 3  # image aspect ratio
    b = np.sqrt(k * (1 / r))
    a = b * r
    a, b = int(np.ceil(a)), int(np.ceil(b))

    img = Image.new('RGBA', (a, b))
    img.putdata(data)
    img = img.resize((1600, 1200), resample=Image.BOX)
    img.save(filename)


# helper converter method
def toInt(number: float) -> int:
    return int(round(number))


if __name__ == "__main__":
    # open data
    dat = ReadFile("alice29.txt")
    # gzip compress data
    gz_dat = list(gzip.compress(dat))
    dat = list(dat)

    print("Original data size:", len(dat))
    print("Compressed data size:", len(gz_dat))

    dat = np.array(dat)
    gz_dat = np.array(gz_dat)

    print("Normalizing Original")
    normDat = BitstreamNormalizeRGB(dat)

    print("Normalizing GZipped")
    norm_gz_Dat = BitstreamNormalizeRGB(gz_dat)

    print("Processing uncompressed image")
    save_img([(toInt(r), 0, 0, 255) for r in normDat], "uncompressed_heat.png")

    print("Processing gzip compressed image")
    save_img([(toInt(r), 0, 0, 255) for r in norm_gz_Dat], "gzip_heat.png")

    print("Combining data")
    fin = []
    for i in norm_gz_Dat:
        fin.append((0, 0, toInt(i), 255))
    for i in normDat:
        fin.append((toInt(i), 0, 0, 255))

    print("Processing combined image")
    save_img(fin, "combined_heat.png")
