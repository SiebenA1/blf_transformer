# -*- coding: utf-8 -*-
import tempfile
from pathlib import Path

import pytest

from blf_converter.common.utils import check_output_file_exists


@pytest.fixture(scope="function")
def valid_file_name():
    """
    Fixture function to yield a valid file name

    Yields
    -------
    str
        The valid file name
    """
    yield "dummy_path.csv"


@pytest.fixture(scope='function')
def valid_output_dir():
    """
    Fixture function to yield an output directory

    Yields
    -------
    Path
        The output directory
    """
    yield Path('tests/testdata')


@pytest.fixture(scope='function')
def invalid_output_dir():
    """
    Fixture function to yield an invalid output directory

    Yields
    -------
    Path
        The invalid output directory
    """
    yield Path('testdata/invalid')


class TestCheckOutputFileExists:
    """
    Test the check_output_file_exists() function
    """

    def test_check_output_file_exists_valid_path_with_yes(self, valid_output_dir, valid_file_name, monkeypatch) -> None:
        """
        Test the check_output_file_exists() function with a valid file path and 'y' input
        """
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        assert check_output_file_exists(valid_output_dir, valid_file_name) is True

    def test_check_output_file_exists_valid_path_with_no(self, monkeypatch) -> None:
        """
        Test the check_output_file_exists() function with a valid file path and 'n' input
        """
        with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.csv') as temp_file:
            valid_output_dir = Path(temp_file.name).parent
            valid_file_name = Path(temp_file.name).name
        monkeypatch.setattr('builtins.input', lambda _: 'n')
        assert check_output_file_exists(valid_output_dir, valid_file_name) is False

    def test_check_output_file_exists_invalid_file_path_without_output_dir(self, invalid_output_dir,
                                                                           valid_file_name) -> None:
        """
        Test the check_output_file_exists() function with an invalid file path without an output directory
        """
        assert check_output_file_exists(invalid_output_dir, valid_file_name) is True
