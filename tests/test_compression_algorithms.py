from src.algorithmForNN.compressUtils import FIC, LZW

import os

import pytest


def test_compress_decompress_LZW_text_from_file():
    path_to_file = "tests/data/text.txt"
    with open(path_to_file, "r") as file:
        start_text = file.read()
        end_text = LZW.decompress(LZW.compress(start_text))

        assert start_text == end_text


def test_compress_decompress_FIC_list():
    start_list = [1, 4, 3, 250, 4056, 10, 128, 1024, 253, 13, 53]
    end_list = FIC.decompress(FIC.compress(start_list))

    assert start_list == end_list


def test_full_compress_decompress_simple_string():
    start_string = "Skoltech is the best"
    payload = LZW.compress(start_string)
    payload = FIC.compress(payload)

    data = FIC.decompress(payload)
    end_string = LZW.decompress(data)

    assert start_string == end_string


def test_compress_decompress_text_from_file():
    path_to_file = "tests/data/text.txt"
    with open(path_to_file, "r") as file:
        start_text = file.read()
        end_text = LZW.decompress(
            FIC.decompress(FIC.compress(LZW.compress(start_text)))
        )

        assert start_text == end_text
