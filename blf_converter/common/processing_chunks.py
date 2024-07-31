# -*- coding: utf-8 -*-
import mmap
from collections import defaultdict
from pathlib import Path
from typing import List

import can
import cantools

from blf_converter.common.utils import load_dbc_files, merge_dicts, save_signals_to_mdf


def process_chunk(args: tuple) -> tuple[dict, set]:
    """
    Process a chunk of messages from a BLF file.

    Parameters
    ----------
    args : tuple
        Tuple containing the database, chunk of messages and the signal list.

    Returns
    -------
    tuple
        A tuple containing a dictionary of signals and a set of found signals.
    """
    db, chunk, signal_list = args
    signals_dict = defaultdict(list)
    found_signals = set()
    for msg in chunk:
        try:
            decoded_msg = db.decode_message(msg.arbitration_id, msg.data)
            timestamp = msg.timestamp
            for signal_name, signal_value in decoded_msg.items():
                if signal_name in signal_list:
                    found_signals.add(signal_name)
                    if isinstance(signal_value, float):
                        signals_dict[signal_name].append((timestamp, format(signal_value, '.3f')))
                    else:
                        signals_dict[signal_name].append((timestamp, str(signal_value)))
        except (cantools.database.errors.Error, KeyError):
            continue
    return signals_dict, found_signals


def read_blf_file(filename: Path, dbc_files: List[Path], chunk_size: int, output_filename: Path,
                  signal_list: List) -> Path:
    """
    Read a BLF file in chunks and process the data.

    Parameters
    ----------
    filename : Path
        Path to the BLF file.
    dbc_files : List[Path]
        List of paths to the DBC files.
    chunk_size : int
        The size of the chunk to process.
    output_filename : Path
        Output filename for the MDF file.
    signal_list : List
        List of signals to decode.

    Returns
    -------
    Path
        Path to the output MDF file.
    """
    db = load_dbc_files(dbc_files)

    with open(filename, 'rb') as f:
        mapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        log = can.BLFReader(mapped_file)  # type: ignore

        chunks = []
        chunk = []
        for msg in log:
            chunk.append(msg)
            if len(chunk) >= chunk_size:
                chunks.append((db, chunk, signal_list))
                chunk = []

        if chunk:
            chunks.append((db, chunk, signal_list))

        mapped_file.close()

    # with Pool(num_workers) as pool:
    #     results = pool.map(process_chunk, chunks)

    results = list(map(process_chunk, chunks))
    signals_dict, found_signals = merge_dicts(results)
    save_signals_to_mdf(signals_dict, output_filename)

    not_found_signals = set(signal_list) - found_signals
    if not_found_signals:
        print(f"The following signals were not found: {', '.join(not_found_signals)}")

    return output_filename
