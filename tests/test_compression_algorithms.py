from src.algorithmForNN.compressUtils import FIC, LZW

import os

import pytest


def test_compress_decompress_LZW_text_from_file():
    path_to_file = "tests/data/dataToCompareFileEncodingCompatibility.txt"
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
    end_string = LZW.decompress(
        FIC.decompress(FIC.compress(LZW.compress(start_string)))
    )

    assert start_string == end_string


def test_coding_compatibility():
    path_to_correct_file = "tests/data/dataGeneratedByJSTool.pcd.labels"
    path_to_test_file = "tests/data/dataToCompareFileEncodingCompatibility.txt"

    with open(path_to_test_file, "r") as test_file, open(
        path_to_correct_file, "rb"
    ) as correct_file:
        test_byte_array = FIC.compress(LZW.compress(test_file.read()))

        correct_byte_array = []
        byte = correct_file.read(1)
        while byte:
            correct_byte_array.append(byte)
            byte = correct_file.read(1)

        assert test_byte_array == correct_byte_array
