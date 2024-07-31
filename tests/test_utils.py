# -*- coding: utf-8 -*-
from pathlib import Path

import pytest

from blf_converter.common.utils import load_dbc_files


@pytest.fixture(scope="function")
def valid_dbc_files():
    """
    Set valid DBC files for testing.

    Yields
    -------
    list
        A list of valid DBC files for testing.
    """
    dbc_files = [
        Path('tests/testdata/ABDRobot_Bus1_export_Crossing.DBC'),
        Path('tests/testdata/E3_1_1_UNECE_CM_E3V_FASCANFD1_KMatrix_V15.04.01.00F_20230727_WL.DBC')
    ]
    yield dbc_files


@pytest.fixture(scope="function")
def invalid_dbc_files():
    """
    Set invalid DBC files for testing.

    Yields
    -------
    list
        A list of invalid DBC files for testing.
    """
    dbc_files = [
        Path('tests/testdata/ABDRobot_Bus1_export_Crossing.DBC'),
        Path('tests/testdata/invalid.dbc')
    ]
    yield dbc_files


class TestLoadDbcFiles:
    """
    UTs for the load_dbc_files function
    """
    def test_load_dbc_files(self, valid_dbc_files):
        """
        Test the load_dbc_files function with valid DBC files.
        """
        load_dbc_files(valid_dbc_files)
        assert True

    def test_load_dbc_files_invalid(self, invalid_dbc_files):
        """
        Test the load_dbc_files function with invalid DBC files.
        """
        with pytest.raises(FileNotFoundError):
            load_dbc_files(invalid_dbc_files)


@pytest.fixture(scope="function")
def valid_path_mapping():
    """
    Set valid path mapping for testing.

    Yields
    -------
    dict
        A valid path mapping for testing.
    """
    path_mapping = {
        'blf_file': Path('tests/testdata/Logging2023-11-21_15-46-47.blf'),
        'dbc_file': [Path('tests/testdata/ABDRobot_Bus1_export_Crossing.DBC')],
        'output_path': Path('test_result')
    }
    yield path_mapping


@pytest.fixture(scope="function")
def invalid_path_mapping_without_output_path():
    """
    Set an invalid path mapping without the output path for testing.

    Yields
    -------
    dict
        An invalid path mapping without the output path for testing.
    """
    path_mapping = {
        'blf_file': Path('tests/testdata/Logging2023-11-21_15-46-47.blf'),
        'dbc_file': [Path('tests/testdata/ABDRobot_Bus1_export_Crossing.DBC')]
    }
    yield path_mapping


@pytest.fixture(scope="function")
def invalid_path_mapping_without_dbc_file():
    """
    Set an invalid path mapping without the DBC file for testing.

    Yields
    -------
    dict
        An invalid path mapping without the DBC file for testing.
    """
    path_mapping = {
        'blf_file': Path('tests/testdata/Logging2023-11-21_15-46-47.blf'),
        'output_path': Path('test_result')
    }
    yield path_mapping


@pytest.fixture(scope="function")
def invalid_path_mapping_without_blf_file():
    """
    Set an invalid path mapping without the BLF file for testing.

    Yields
    -------
    dict
        An invalid path mapping without the BLF file for testing.
    """
    path_mapping = {
        'dbc_file': [Path('tests/testdata/ABDRobot_Bus1_export_Crossing.DBC')],
        'output_path': Path('test_result')
    }
    yield path_mapping
