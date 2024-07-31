# -*- coding: utf-8 -*-
from pathlib import Path

import pytest

from blf_converter.common.blf_converter import BlfConverter


@pytest.fixture(scope='function')
def valid_data_for_test2mf4():
    """Fixture function to yield valid data

    Yields
    -------
    dict
        The valid data for test case
    """
    yield {
        "blf_file": Path("tests/testdata/Logging2023-11-21_15-46-47.blf"),
        "dbc_file": [Path("tests/testdata/E3_1_1_UNECE_CM_E3V_FASCANFD1_KMatrix_V15.04.01.00F_20230727_WL.DBC")],
        "output_path": Path("test_results/export"),
        "signal_list": ['ESC_Fahrerbremswunsch', 'TimeToCollisionLongitudinal'],
        "signal_mapping": {
            "ESC_Fahrerbremswunsch": "ESC_Fahrerbremswunsch",
            "TimeToCollisionLongitudinal": "TimeToCollisionLongitudinal"
        }
    }


@pytest.fixture(scope='module')
def data_with_invalid_blf():
    """Fixture function to yield data with invalid blf

    Yields
    -------
    dict
        The data with invalid blf for test case
    """
    yield {
        "blf_file": Path("tests/testdata/invalid_blf_test.blf"),
        "dbc_file": [Path("tests/testdata/E3_1_1_UNECE_CM_E3V_FASCANFD1_KMatrix_V15.04.01.00F_20230727_WL.DBC")],
        "output_path": Path("test_results/export"),
        "signal_list": ['ESC_Fahrerbremswunsch', 'TimeToCollisionLongitudinal'],
        "signal_mapping": {
            "ESC_Fahrerbremswunsch": "ESC_Fahrerbremswunsch",
            "TimeToCollisionLongitudinal": "TimeToCollisionLongitudinal"
        }
    }


@pytest.fixture(scope='module')
def data_with_invalid_dbc():
    """Fixture function to yield data with invalid dbc

    Yields
    -------
    dict
        The data with invalid dbc for test case
    """
    yield {
        "blf_file": Path("tests/testdata/Logging2023-11-21_15-46-47.blf"),
        "dbc_file": [Path("tests/testdata/invalid_dbc_test.DBC")],
        "output_path": Path("test_results/export"),
        "signal_list": ['ESC_Fahrerbremswunsch', 'TimeToCollisionLongitudinal'],
        "signal_mapping": {
            "ESC_Fahrerbremswunsch": "ESC_Fahrerbremswunsch",
            "TimeToCollisionLongitudinal": "TimeToCollisionLongitudinal"
        }
    }


@pytest.fixture(scope='module')
def data_with_invalid_signal_list():
    """Fixture function to yield data with invalid signal list

    Yields
    -------
    dict
        The data with invalid signal list for test case
    """
    yield {
        "blf_file": Path("tests/testdata/Logging2023-11-21_15-46-47.blf"),
        "dbc_file": [Path("tests/testdata/E3_1_1_UNECE_CM_E3V_FASCANFD1_KMatrix_V15.04.01.00F_20230727_WL.DBC")],
        "output_path": Path("test_results/export"),
        "signal_list": {},
        "signal_mapping": {
            "ESC_Fahrerbremswunsch": "ESC_Fahrerbremswunsch",
            "TimeToCollisionLongitudinal": "TimeToCollisionLongitudinal"
        }
    }


class TestDecodeBlf2Mf4:
    """
    UTs related to the decode_blf2mf4 function, which decodes the BLF file to a mf4 file.
    """

    def test_decode_blf2mf4_with_valid_input(self, valid_data_for_test2mf4, monkeypatch) -> None:
        """Test function for decode_blf2mf4 with valid input data
        """
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        blf = valid_data_for_test2mf4["blf_file"]
        dbc = valid_data_for_test2mf4["dbc_file"]
        output_path = valid_data_for_test2mf4["output_path"]
        signal_list = valid_data_for_test2mf4["signal_list"]
        signal_mapping = valid_data_for_test2mf4["signal_mapping"]
        blf_converter = BlfConverter(blf, dbc, output_path, signal_list, signal_mapping)
        output = blf_converter.decode_blf2mf4()
        assert output == Path("test_results/export/mf4/Logging2023-11-21_15-46-47.mf4")

    def test_decode_blf2mf4_with_invalid_blf(self, data_with_invalid_blf) -> None:
        """Test function for decode_blf2mf4 with invalid blf file
        """
        with pytest.raises(BaseException):
            blf = data_with_invalid_blf["blf_file"]
            dbc = data_with_invalid_blf["dbc_file"]
            output_path = data_with_invalid_blf["output_path"]
            signal_list = data_with_invalid_blf["signal_list"]
            signal_mapping = data_with_invalid_blf["signal_mapping"]
            blf_converter = BlfConverter(blf, dbc, output_path, signal_list, signal_mapping)
            blf_converter.decode_blf2mf4()

    def test_decode_blf2mf4_with_invalid_dbc(self, data_with_invalid_dbc) -> None:
        """Test function for decode_blf2mf4 with invalid dbc file
        """
        with pytest.raises(BaseException):
            blf = data_with_invalid_dbc["blf_file"]
            dbc = data_with_invalid_dbc["dbc_file"]
            output_path = data_with_invalid_dbc["output_path"]
            signal_list = data_with_invalid_dbc["signal_list"]
            signal_mapping = data_with_invalid_dbc["signal_mapping"]
            blf_converter = BlfConverter(blf, dbc, output_path, signal_list, signal_mapping)
            blf_converter.decode_blf2mf4()

    def test_decode_blf2mf4_with_invalid_signal_list(self, data_with_invalid_signal_list) -> None:
        """Test function for decode_blf2mf4 with invalid signal list
        """
        with pytest.raises(BaseException):
            blf = data_with_invalid_signal_list["blf_file"]
            dbc = data_with_invalid_signal_list["dbc_file"]
            output_path = data_with_invalid_signal_list["output_path"]
            signal_list = data_with_invalid_signal_list["signal_list"]
            signal_mapping = data_with_invalid_signal_list["signal_mapping"]
            blf_converter = BlfConverter(blf, dbc, output_path, signal_list, signal_mapping)
            blf_converter.decode_blf2mf4()


@pytest.fixture(scope='function')
def valid_data_for_test2csv():
    """
    Fixture function to yield valid data

    Yields
    -------
    dict
        The valid data for test case
    """
    yield {
        "blf_file": Path("tests/testdata/Logging2023-11-21_15-46-47.blf"),
        "dbc_file": [Path("tests/testdata/E3_1_1_UNECE_CM_E3V_FASCANFD1_KMatrix_V15.04.01.00F_20230727_WL.DBC")],
        "output_path": Path("test_results/export"),
        "signal_list": ['ESC_Fahrerbremswunsch', 'TimeToCollisionLongitudinal'],
        "signal_mapping": {
            "ESC_Fahrerbremswunsch": "ESC_Fahrerbremswunsch",
            "TimeToCollisionLongitudinal": "TimeToCollisionLongitudinal"
        }
    }


class TestDecodeBlf2csv:
    """
    UTs related to the decode_blf2csv function, which decodes the BLF file to a csv file.
    """

    def test_decode_blf2csv_with_valid_input(self, valid_data_for_test2csv, monkeypatch) -> None:
        """Test function for decode_blf2csv with valid input data
        """
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        blf = valid_data_for_test2csv["blf_file"]
        dbc = valid_data_for_test2csv["dbc_file"]
        output_path = valid_data_for_test2csv["output_path"]
        signal_list = valid_data_for_test2csv["signal_list"]
        signal_mapping = valid_data_for_test2csv["signal_mapping"]
        blf_converter = BlfConverter(blf, dbc, output_path, signal_list, signal_mapping)
        output = blf_converter.decode_blf2csv()
        csv_files = list(output.glob('*.csv'))
        assert len(csv_files) >= 1

    def test_decode_blf2csv_with_invalid_blf(self, data_with_invalid_blf) -> None:
        """Test function for decode_blf2csv with invalid blf file
        """
        with pytest.raises(BaseException):
            blf = data_with_invalid_blf["blf_file"]
            dbc = data_with_invalid_blf["dbc_file"]
            output_path = data_with_invalid_blf["output_path"]
            signal_list = data_with_invalid_blf["signal_list"]
            signal_mapping = data_with_invalid_blf["signal_mapping"]
            blf_converter = BlfConverter(blf, dbc, output_path, signal_list, signal_mapping)
            blf_converter.decode_blf2csv()

    def test_decode_blf2csv_with_invalid_dbc(self, data_with_invalid_dbc, monkeypatch) -> None:
        """Test function for decode_blf2csv with invalid dbc file
        """
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        with pytest.raises(BaseException):
            blf = data_with_invalid_dbc["blf_file"]
            dbc = data_with_invalid_dbc["dbc_file"]
            output_path = data_with_invalid_dbc["output_path"]
            signal_list = data_with_invalid_dbc["signal_list"]
            signal_mapping = data_with_invalid_dbc["signal_mapping"]
            blf_converter = BlfConverter(blf, dbc, output_path, signal_list, signal_mapping)
            blf_converter.decode_blf2csv()

    def test_decode_blf2csv_with_invalid_signal_list(self, data_with_invalid_signal_list, monkeypatch) -> None:
        """Test function for decode_blf2csv with invalid signal list
        """
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        with pytest.raises(ValueError):
            blf = data_with_invalid_signal_list["blf_file"]
            dbc = data_with_invalid_signal_list["dbc_file"]
            output_path = data_with_invalid_signal_list["output_path"]
            signal_list = data_with_invalid_signal_list["signal_list"]
            signal_mapping = data_with_invalid_signal_list["signal_mapping"]
            blf_converter = BlfConverter(blf, dbc, output_path, signal_list, signal_mapping)
            blf_converter.decode_blf2csv()
