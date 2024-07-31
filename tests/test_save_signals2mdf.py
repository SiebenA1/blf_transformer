# -*- coding: utf-8 -*-
from pathlib import Path

import pytest

from blf_converter.common.utils import save_signals_to_mdf


@pytest.fixture(scope='function')
def data_with_valid_signals():
    """
    Fixture function to yield data with valid signals
    """
    yield {
        'signal1': [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0)],
        'signal2': [(0.0, 'a'), (1.0, 'b'), (2.0, 'c')]
    }


@pytest.fixture(scope='function')
def data_with_empty_signals():
    """
    Fixture function to yield data with invalid signals
    """
    yield None, {}


@pytest.fixture(scope='function')
def data_with_invalid_signals_not_dict():
    """
    Fixture function to yield data with invalid signals
    """
    yield [
        (1, [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0)]),
        (2, [(0.0, 'a'), (1.0, 'b'), (2.0, 'c')])
    ]


class TestSaveSignalsToMF4:
    """
    UTs for the save_signals_to_mdf() function
    """

    def test_save_signals_to_mdf_valid_signals(self, data_with_valid_signals: dict) -> None:
        """
        Test the save_signals_to_mdf() function with valid signals
        """
        output_filename = Path('test_results/output.mf4')
        save_signals_to_mdf(data_with_valid_signals, output_filename)
        assert output_filename.is_file()

    def test_save_signals_to_mdf_empty_signals(self, data_with_empty_signals) -> None:
        """
        Test the save_signals_to_mdf() function with empty signals
        """
        output_filename = Path('test_results/output.mf4')
        with pytest.raises(ValueError):
            save_signals_to_mdf(data_with_empty_signals, output_filename)

    def test_save_signals_to_mdf_invalid_signals_not_dict(self, data_with_invalid_signals_not_dict) -> None:
        """
        Test the save_signals_to_mdf() function with invalid signals
        """
        output_filename = Path('test_results/output.mf4')
        with pytest.raises(ValueError):
            save_signals_to_mdf(data_with_invalid_signals_not_dict, output_filename)
