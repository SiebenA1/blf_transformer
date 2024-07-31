# -*- coding: utf-8 -*-
from collections import defaultdict
from pathlib import Path
from typing import List

import cantools
from asammdf import MDF, Signal


def validate_results(results: List[tuple[dict, set]]) -> bool:
    """
    Validate the result from the processing of the chunks.

    Parameters
    ----------
    results : List[tuple[dict, set]]
        List of tuples containing a dictionary of signals and a set of found signals.

    Returns
    -------
    bool
        True if the result is valid, False otherwise.
    """
    if not isinstance(results, list):
        return False

    for item in results:
        if not isinstance(item, tuple) or len(item) != 2:
            return False
        signals_dict, found_set = item
        if not isinstance(signals_dict, dict) or not isinstance(found_set, set):
            return False
    return True


def merge_dicts(results: List[tuple[dict, set]]) -> tuple[dict, set]:
    """
    Merge the results of multiple chunks into a single dictionary.

    Parameters
    ----------
    results : List[tuple[dict, set]]
        List of tuples containing a dictionary of signals and a set of found signals.

    Returns
    -------
    tuple: [dict, set]
        A tuple containing a merged dictionary of signals and a set of found signals.
    """
    results_validation = validate_results(results)
    if not results_validation:
        raise ValueError("Please provide a list of tuples with a dictionary and a set.")
    merged_dict = defaultdict(list)
    found_signals = set()
    for signals_dict, found_set in results:
        for k, v in signals_dict.items():
            merged_dict[k].extend(v)
        found_signals.update(found_set)
    return merged_dict, found_signals


def save_signals_to_mdf(signals_dict: dict, output_filename: Path, append: bool = True) -> None:
    """
    Save the signals to an MDF file.

    Parameters
    ----------
    signals_dict : dict
        Dictionary containing the signals.
    output_filename : Path
        Output filename for the MDF file.
    append : bool
        Whether to append to an existing file.
    """
    if signals_dict is None or not signals_dict:
        raise ValueError("Signals are empty.")
    elif not isinstance(signals_dict, dict):
        raise ValueError("Signals are illegally formatted.")
    mdf = MDF(version='4.10')
    for signal_name, signal_data in signals_dict.items():
        timestamps, values = zip(*signal_data)
        first_value = values[0]
        if isinstance(first_value, str):
            signal = Signal(samples=values, timestamps=timestamps, name=signal_name, encoding='utf-8')
        else:
            signal = Signal(samples=values, timestamps=timestamps, name=signal_name)
        mdf.append(signal)
    mdf.save(output_filename, overwrite=not append)


def check_output_file_exists(output_dir: Path, filename: str) -> bool:
    """
    Check if the output file already exists.

    Parameters
    ------------

    output_dir : Path
        The output directory.
    filename : str
        The filename to check.

    Returns
    -----------
    bool
        True if the file does not exist or need to be re-converted, False abort.
    """
    output_file = output_dir / filename

    if output_file.is_file():
        continue_process = input(f"File {output_file} already exists. Do you want to overwrite it? (y/n):")
        if continue_process.lower() == 'y':
            return True
        else:
            return False
    else:
        return True


def load_dbc_files(dbc_files: List[Path]):
    """
    Load multiple DBC files into a database.

    Parameters
    ------------
    dbc_files : list
        The list of paths to the DBC files.

    Returns
    -----------
    cantools.database.Database
        The database object containing the loaded DBC files.
    """
    db = cantools.database.Database()
    for dbc_file in dbc_files:
        db.add_dbc_file(dbc_file)
    return db


def validate_paths(blf_path: Path, dbc_path: list, export_path: Path) -> dict[str, str | bool]:
    """
    Validate the provided paths for the converter function.

    Parameters
    ------------
    blf_path: Path
        Path of the BLF file.
    export_path: Path
        Path of the export directory.
    dbc_path: List
        List of paths to the DBC files

    Returns
    -----------
        Dict with the validation result and status message.
    """
    blf_path = blf_path
    dbc_path = dbc_path
    export_path = export_path
    if blf_path is None or not blf_path.is_file():
        return {"success": False, "message": "The BLF file does not exist."}
    if dbc_path is None:
        return {"success": False, "message": "The DBC file is not provided."}
    else:
        for dbc in dbc_path:
            if dbc is None or not dbc.is_file():
                return {"success": False, "message": "The DBC file is not provided."}

    if export_path is None:
        return {"success": False, "message": "The export path is not provided."}

    else:
        return {"success": True, "message": "Paths are valid."}
