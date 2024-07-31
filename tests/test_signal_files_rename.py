# -*- coding: utf-8 -*-
from pathlib import Path
import pytest

from unittest.mock import patch, mock_open
import pandas as pd

from blf_converter.module.signal_files_rename import CSVFileRenamer


@pytest.fixture(scope='module')
def signal_mapping():
    """
    A fixture to return a signal mapping dictionary.

    Returns
    -------
    dict
    """
    return {
        "col1": "signal1",
        "col2": "signal2",
        "col3": "signal3"
    }


@pytest.fixture(scope='function')
def mock_csv_file_with_columns():
    """A fixture to return a mock CSV file with valid columns.
    """
    return "col1,col2,col3\n"


@pytest.fixture(scope='function')
def mock_csv_file_with_one_column():
    """A fixture to return a mock CSV file with one column.
    """
    return "col1\n"


@pytest.fixture(scope='function')
def mock_csv_file_empty():
    """A fixture to return a mock empty CSV file.
    """
    return ""


class TestGetSignalName:
    """
    UTs for the get_signal_name method in CSVFileRenamer class.
    """
    def test_get_signal_name_with_valid_columns(self, mock_csv_file_with_columns, tmp_path, signal_mapping) -> None:
        """
        Test get_signal_name method with valid columns.

        Parameters
        ----------
        mock_csv_file_with_columns : str
        """
        with (patch("builtins.open", mock_open(read_data=mock_csv_file_with_columns)), patch(
                "pandas.read_csv") as mock_read_csv):
            mock_read_csv.return_value = pd.DataFrame(columns=["signal1", "signal2", "signal3"])
            renamer = CSVFileRenamer(tmp_path, signal_mapping)
            result = renamer._get_signal_name(csv_file_path=Path("tests/testdata/dummy_path.csv"),
                                              signal_mapping=signal_mapping)
            assert result == "col2"

    def test_get_signal_name_with_one_column(self, mock_csv_file_with_one_column, tmp_path, signal_mapping) -> None:
        """
        Test get_signal_name method with one column.

        Parameters
        ----------
        mock_csv_file_with_one_column : str
        """
        with patch("builtins.open", mock_open(read_data=mock_csv_file_with_one_column)), patch(
                "pandas.read_csv") as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame(columns=["col1"])
            renamer = CSVFileRenamer(tmp_path, signal_mapping)
            result = renamer._get_signal_name(csv_file_path=Path("tests/testdata/dummy_path.csv"),
                                              signal_mapping=signal_mapping)
            assert result is False

    def test_get_signal_name_with_empty_file(self, mock_csv_file_empty, signal_mapping, tmp_path) -> None:
        """
        Test get_signal_name method with empty file.

        Parameters
        ----------
        mock_csv_file_empty
        """
        with patch("builtins.open", mock_open(read_data=mock_csv_file_empty)), patch(
                "pandas.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = pd.errors.EmptyDataError("No columns to parse from file")
            renamer = CSVFileRenamer(tmp_path, signal_mapping)
            result = renamer._get_signal_name(csv_file_path=Path("tests/testdata/dummy_path.csv"),
                                              signal_mapping=signal_mapping)
            assert result is False

    def test_get_signal_name_with_read_error(self, signal_mapping, tmp_path) -> None:
        """
        Test get_signal_name method with read error.
        """
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = Exception("Read error")
            renamer = CSVFileRenamer(tmp_path, signal_mapping)
            result = renamer._get_signal_name(csv_file_path=Path("tests/testdata/dummy_path.csv"),
                                              signal_mapping=signal_mapping)
            assert result is False


@pytest.fixture(scope='function')
def mock_directory(tmp_path: Path) -> Path:
    """
    A fixture to create a mock directory for testing.

    Parameters
    ----------
    tmp_path: Path

    Returns
    -------
    Path
    """
    (tmp_path / 'csv').mkdir()
    return Path(tmp_path)


@pytest.fixture(scope='function')
def file_renamer(mock_directory: Path, signal_mapping) -> CSVFileRenamer:
    """
    A fixture to return a CSVFileRenamer object.

    Parameters
    ----------
    signal_mapping: dict
    mock_directory: Path

    Returns
    -------
    CSVFileRenamer: object
    """
    return CSVFileRenamer(mock_directory, signal_mapping)


@pytest.fixture(scope='function')
def valid_mock_csv_file(tmp_path: Path) -> Path:
    """
    A fixture to create a mock CSV file with valid columns.

    Parameters
    ----------
    tmp_path: Path

    Returns
    -------
    Path
    """
    file_path = tmp_path / 'test1.csv'
    file_path.write_text("col1,col2\n1,2\n")
    return file_path


@pytest.fixture(scope='function')
def invalid_mock_csv_file(tmp_path: Path) -> Path:
    """
    A fixture to create a mock CSV file with invalid columns.

    Parameters
    ----------
    tmp_path: Path

    Returns
    -------
    Path
    """
    file_path = tmp_path / 'test2.csv'
    file_path.write_text("col1\n1\n")
    return file_path


@pytest.fixture(scope='function')
def invalid_mock_csv_file_no_columns(tmp_path: Path) -> Path:
    """
    A fixture to create a mock CSV file with no columns.

    Parameters
    ----------
    tmp_path: Path

    Returns
    -------
    Path
    """
    file_path = tmp_path / 'test3.csv'
    file_path.write_text("")
    return file_path


class TestCSVFileRenamer:
    """
    UTs for file_rename in CSVFileRenamer class
    """
    def test_rename_files_with_valid_columns(self, file_renamer, valid_mock_csv_file) -> None:
        """
        Test rename_files method with valid columns in data file.

        Parameters
        ----------
        file_renamer
        valid_mock_csv_file
        """
        output = file_renamer.rename_files()
        assert output is True

    def test_rename_files_with_one_column(self, file_renamer, invalid_mock_csv_file_no_columns) -> None:
        """
        Test rename_files method with one column in data file.

        Parameters
        ----------
        file_renamer
        invalid_mock_csv_file_no_columns
        """
        output = file_renamer.rename_files()
        assert output is False

    def test_rename_files_with_invalid_file(self, file_renamer, invalid_mock_csv_file) -> None:
        """
        Test rename_files method with invalid columns in data file.

        Parameters
        ----------
        file_renamer
        invalid_mock_csv_file
        """
        output = file_renamer.rename_files()
        assert output is False
