# -*- coding: utf-8 -*-
"""A test module for merge_dicts and validate_results functions of test_save_signals2mdf module
"""
import pytest

from blf_converter.common.utils import merge_dicts, validate_results


@pytest.fixture(scope='function')
def data_with_valid_results():
    """
    Fixture function to yield data with valid results

    Yields
    -------
    list
        The data with valid results for test case
    """
    yield [
        (
            {"signal1": [(1, 1), (2, 2)], "signal2": [(3, 3), (4, 4)]},
            {"signal1", "signal2"}
        ),
        (
            {"signal3": [(5, 5), (6, 6)], "signal4": [(7, 7), (8, 8)]},
            {"signal3", "signal4"}
        )
    ]


@pytest.fixture(scope='function')
def data_with_empty_results():
    """
    Fixture function to yield data with empty results

    Yields
    -------
    list
        The data with empty results for test case
    """
    yield [
        ({}, set()),
        ({}, set())
    ]


@pytest.fixture(scope='function')
def data_with_invalid_results_not_list():
    """
    Fixture function to yield data with invalid results

    Yields
    -------
    dict
        The data with invalid results for test case
    """
    yield {
        "a":
            (
                {"signal1": [(1, 1), (2, 2)], "signal2": [(3, 3), (4, 4)]},
                {"signal1", "signal2"}
            ),
        "b":
            (
                {"signal3": [(5, 5), (6, 6)], "signal4": [(7, 7), (8, 8)]},
                {"signal3", "signal4"}
            )
    }


@pytest.fixture(scope='function')
def data_with_invalid_results_not_tuple():
    """
    Fixture function to yield data with invalid results

    Yields
    -------
    list
        The data with invalid results format for test case
    """
    yield [
        {"signal1": [(1, 1), (2, 2)], "signal2": [(3, 3), (4, 4)]},
        {"signal3": [(5, 5), (6, 6)], "signal4": [(7, 7), (8, 8)]}
    ]


@pytest.fixture(scope='function')
def data_with_invalid_results_not_dict():
    """
    Fixture function to yield data with invalid results

    Yields
    -------
    list
        The data with invalid results format for test case
    """
    yield [
        (
            "a",
            {"signal1", "signal2"}
        ),
        (
            "b",
            {"signal3", "signal4"}
        )
    ]


@pytest.fixture(scope='function')
def data_with_invalid_results_not_set():
    """
    Fixture function to yield data with invalid results

    Yields
    -------
    list
        The data with invalid results format for test case
    """
    yield [
        (
            {"signal1": [(1, 1), (2, 2)], "signal2": [(3, 3), (4, 4)]},
            "a"
        ),
        (
            {"signal3": [(5, 5), (6, 6)], "signal4": [(7, 7), (8, 8)]},
            "b"
        )
    ]


class TestDataMergeModule:
    """
    UTs related to the merge_dicts function, which merges the results of multiple chunks into a single dictionary.
    """

    def test_merge_dicts(self, data_with_valid_results) -> None:
        """Test the merge_dicts function with valid results.
        """
        expected_merged_dict = {
            "signal1": [(1, 1), (2, 2)],
            "signal2": [(3, 3), (4, 4)],
            "signal3": [(5, 5), (6, 6)],
            "signal4": [(7, 7), (8, 8)]
        }
        expected_found_signals = {"signal1", "signal2", "signal3", "signal4"}

        merged_dict, found_signals = merge_dicts(data_with_valid_results)

        assert merged_dict == expected_merged_dict
        assert found_signals == expected_found_signals

    def test_merge_dicts_with_empty_results(self, data_with_empty_results) -> None:
        """Test the merge_dicts function with empty results.
        """
        expected_merged_dict: dict = {}
        expected_found_signals: set = set()

        merged_dict, found_signals = merge_dicts(data_with_empty_results)

        assert merged_dict == expected_merged_dict
        assert found_signals == expected_found_signals


class TestResultsValidation:
    """
    UTs related to the validate_results function, which validates the results of multiple chunks.
    """

    def test_validate_results_with_valid_results(self, data_with_valid_results) -> None:
        """Test the validate_results function with valid results.
        """
        results_validation = validate_results(data_with_valid_results)
        assert results_validation is True

    def test_validate_results_with_invalid_results_not_list(self, data_with_invalid_results_not_list) -> None:
        """Test the validate_results function with invalid results, which was not a list.
        """
        results_validation = validate_results(data_with_invalid_results_not_list)
        assert results_validation is False

    def test_validate_results_with_invalid_results_not_tuple(self, data_with_invalid_results_not_tuple) -> None:
        """Test the validate_results function with invalid results, which has no tuple.
        """
        results_validation = validate_results(data_with_invalid_results_not_tuple)
        assert results_validation is False

    def test_validate_results_with_invalid_results_not_dict(self, data_with_invalid_results_not_dict) -> None:
        """Test the validate_results function with invalid results, which has no dict.
        """
        results_validation = validate_results(data_with_invalid_results_not_dict)
        assert results_validation is False

    def test_validate_results_with_invalid_results_not_set(self, data_with_invalid_results_not_set) -> None:
        """Test the validate_results function with invalid results, which has no set.
        """
        results_validation = validate_results(data_with_invalid_results_not_set)
        assert results_validation is False
