import json
from unittest.mock import mock_open, patch

import pytest

from nist_tests import (
    bit_frequency_test,
    consecutive_bit_test,
    longest_run_of_ones_test,
)


c_sequence = "01110000001111111111111110100011110001110111000101110100110001001110010100101100001101111000110101000000010101011111011111001001"
mock_data = '{"java": "11011001"}'
mock_results = {
    "Bit Frequency Test": 0.4795001221869535,
    "Consecutive Bit Test": 0.8504362683123465,
    "Longest Run of Ones Test": 0.002682392443551449
}
orig_results = {
    "Bit Frequency Test": 0.05182992721790971,
    "Consecutive Bit Test": 0.9841043891445014,
    "Longest Run of Ones Test": 0.4798166969631381
}

def test_bit_frequency():
    frequency = 0.2888443663464849
    assert bit_frequency_test(c_sequence) == pytest.approx(frequency)

def test_consecutive_bit_test():
    frequency = 0.13238091404604369
    assert consecutive_bit_test(c_sequence) == pytest.approx(frequency)

def test_longest_run_of_ones_test():
    frequency = 0.5358121524014012
    assert pytest.approx(frequency) == longest_run_of_ones_test(c_sequence)


@pytest.mark.parametrize(
        "name, value", 
        [("java", orig_results["Bit Frequency Test"])]
        )
def test_bit_frequency_test_w_r(name, value):
    file_path = "lab_5/gen_results.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    sequence = data[name]
    frequency = bit_frequency_test(sequence)
    assert frequency == pytest.approx(value)

@pytest.mark.parametrize(
        "name, value", 
        [("java", mock_results["Bit Frequency Test"])]
        )
def test_bit_frequency_test_w_r_m(name, value):
    with patch("builtins.open", mock_open(read_data=mock_data)):
        file_path = "mocked_path/gen_results.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    sequence = data[name]
    frequency = bit_frequency_test(sequence)
    assert frequency == pytest.approx(value)

@pytest.mark.parametrize(
        "name, value", 
        [("java", orig_results["Consecutive Bit Test"])]
        )
def test_consecutive_bit_test_w_r(name, value):
    file_path = "lab_5/gen_results.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    sequence = data[name]
    frequency = consecutive_bit_test(sequence)
    assert frequency == pytest.approx(value)

@pytest.mark.parametrize(
        "name, value", 
        [("java", mock_results["Consecutive Bit Test"])]
        )
def test_consecutive_bit_test_w_r_m(name, value):
    with patch("builtins.open", mock_open(read_data=mock_data)):
        file_path = "mocked_path/gen_results.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    sequence = data[name]
    frequency = consecutive_bit_test(sequence)
    assert frequency == pytest.approx(value)

@pytest.mark.parametrize(
        "name, value", 
        [("java", orig_results["Longest Run of Ones Test"])]
        )
def test_longest_run_of_ones_test_w_r_m(name, value):
    file_path = "lab_5/gen_results.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    sequence = data[name]
    frequency = longest_run_of_ones_test(sequence)
    assert frequency == pytest.approx(value)

@pytest.mark.parametrize(
        "name, value", 
        [("java", mock_results["Longest Run of Ones Test"])]
        )
def test_longest_run_of_ones_test_w_r(name, value):
    with patch("builtins.open", mock_open(read_data=mock_data)):
        file_path = "mocked_path/gen_results.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    sequence = data[name]
    frequency = longest_run_of_ones_test(sequence)
    assert frequency == pytest.approx(value)