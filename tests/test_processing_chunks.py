# -*- coding: utf-8 -*-
from pathlib import Path

import cantools
import pytest
from unittest.mock import Mock

from blf_converter.common.processing_chunks import process_chunk, read_blf_file


class MockMessage:
    """
    A mock class for the message object.
    """
    def __init__(self, arbitration_id, data, timestamp):
        self.arbitration_id = arbitration_id
        self.data = data
        self.timestamp = timestamp


@pytest.fixture(scope='function')
def valid_mock_db():
    """
    A mock database object with valid data.

    Returns
    -------
    Mock
        A mock object for the database.
    """
    db = Mock()
    db.decode_message = Mock(side_effect=[
        {'signal1': 1.234, 'signal2': 5},
        {'signal1': 2.345, 'signal3': 'text'}
    ])
    return db


@pytest.fixture(scope='function')
def invalid_mock_db():
    """
    A mock database object with invalid data.

    Returns
    -------
    Mock
        A mock object for the database.
    """
    db = Mock()
    db.decode_message = Mock(side_effect=[
        cantools.database.errors.Error,
        KeyError
    ])
    return db


@pytest.fixture(scope='function')
def valid_chunk():
    """
    A valid chunk of data.

    Returns
    -------
    list
        A list of mock messages.
    """
    return [
        MockMessage(1, b'\x00\x01', 0.1),
        MockMessage(2, b'\x02\x03', 0.2)
    ]


@pytest.fixture(scope='function')
def signal_list():
    """
    A list of valid signals.

    Returns
    -------
    list
        A list of signals.
    """
    return ['signal1', 'signal2']


@pytest.fixture(scope='function')
def invalid_signal_list():
    """
    A list of invalid signals.

    Returns
    -------
    list
        A list of signals.
    """
    return ['signal4']


@pytest.fixture(scope='function')
def expected_results():
    """
    Expected results for the process_chunk function.

    Returns
    -------
    tuple
        A tuple containing the expected signals dictionary and the expected found signals.
    """
    expected_signals_dict = {
        'signal1': [(0.1, '1.234'), (0.2, '2.345')],
        'signal2': [(0.1, '5')]
    }
    expected_found_signals = {'signal1', 'signal2'}
    return expected_signals_dict, expected_found_signals


class TestProcessChunk:
    """
    UTs for the process_chunk function.
    """
    def test_process_chunk_with_valid_data(self, valid_mock_db: Mock, valid_chunk: list, signal_list: list, expected_results: tuple) -> None:
        """
        Test the process_chunk function with valid data.

        Parameters
        ----------
        valid_mock_db
        valid_chunk
        signal_list
        expected_results
        """
        expected_signals_dict, expected_found_signals = expected_results
        result_signals_dict, result_found_signals = process_chunk((valid_mock_db, valid_chunk, signal_list))

        assert result_signals_dict == expected_signals_dict
        assert result_found_signals == expected_found_signals

    def test_process_chunk_with_invalid_db(self, invalid_mock_db: Mock, valid_chunk: list, signal_list: list) -> None:
        """
        Test the process_chunk function with an invalid database.

        Parameters
        ----------
        invalid_mock_db
        valid_chunk
        signal_list
        """
        result_signals_dict, result_found_signals = process_chunk((invalid_mock_db, valid_chunk, signal_list))

        assert result_signals_dict == {}
        assert result_found_signals == set()

    def test_process_chunk_with_invalid_signal(self, valid_mock_db: Mock, valid_chunk: list, invalid_signal_list: list) -> None:
        """
        Test the process_chunk function with an invalid signal.

        Parameters
        ----------
        valid_mock_db
        valid_chunk
        invalid_signal_list
        """
        result_signals_dict, result_found_signals = process_chunk((valid_mock_db, valid_chunk, invalid_signal_list))

        assert result_signals_dict == {}
        assert result_found_signals == set()


@pytest.fixture(scope='function')
def valid_data():
    """
    Valid data for the read_blf_file

    Yields
    ------
    dict
        A dictionary containing the valid data.
    """
    valid_input = {
        'filename': Path('tests/testdata/Logging2023-11-21_15-46-47.blf'),
        'dbc_files': [Path('tests/testdata/E3_1_1_UNECE_CM_E3V_FASCANFD1_KMatrix_V15.04.01.00F_20230727_WL.DBC')],
        'chunk_size': 150000,
        'output_filename': Path('test_results/Logging2023-11-21_15-46-47.mf4'),
        'signal_list': ['LWI_Lenkradw_Geschw', 'LWI_Lenkradwinkel'],
        'num_workers': 1
    }
    yield valid_input


class TestReadBlfFileInChunks:
    """
    UTs for the read_blf_file function
    """
    def test_read_blf_file_in_chunks(self, valid_data: dict) -> None:
        """
        Test the read_blf_file function.

        Parameters
        ----------
        valid_data
        """
        output = read_blf_file(**valid_data)
        assert output == Path('test_results/Logging2023-11-21_15-46-47.mf4')
