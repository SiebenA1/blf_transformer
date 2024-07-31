# -*- coding: utf-8 -*-
from pathlib import Path

from asammdf import MDF

from blf_converter.common.processing_chunks import read_blf_file
from blf_converter.common.utils import validate_paths
from blf_converter.module.signal_files_rename import CSVFileRenamer


class BlfConverter:
    """
    BlfConverter class to decode BLF files.
    Including methods to decode BLF files to different formats.
    """

    def __init__(self, blf_file: Path, dbc_file: list[Path], signal_list: list[str]):
        """
        Initialize the CustomBLF class.

        Parameters
        ----------
        blf_file : str
            Path to the BLF file.
        dbc_file : List[str]
            List of paths to the DBC files.
        signal_list : List[str]
            List of signals to decode.
        """
        self.blf: Path = blf_file
        self.dbc = dbc_file
        self.signals = signal_list
        validate_paths(self.blf, self.dbc, self.output_path)
        # Set default values for chunk size and RAM size.
        # These values can be adjusted based on the system configuration and data volume.
        self.chunk_size = 150000  # Defines the number of records to process in each chunk.

    @property
    def name(self) -> str:
        """
        Get the name of the BLF file.

        Returns
        -------
        str
            Name of the BLF file without suffix.
        """
        return self.blf.stem

    @property
    def output_path(self) -> Path:
        """
        Get the directory of the BLF file and create a new folder with the same name as the file.

        Returns
        -------
        Path
            output path for the converted files.
        """
        new_dir = self.blf.parent / self.name
        if not new_dir.is_dir():
            new_dir.mkdir(parents=True, exist_ok=True)
        return new_dir

    def _decode_blf2mf4(self) -> Path:
        """
        Decode the BLF file and export the data to an MF4 file.

        Returns
        -------
        Path
            Output .mf4 file.
        """
        self.output_path.joinpath(self.name + ".mf4").unlink(missing_ok=True)
        output_filename = self.output_path / 'mf4' / (self.name + ".mf4")
        mf4_file = read_blf_file(self.blf, self.dbc, self.chunk_size, output_filename, self.signals)
        return mf4_file

    def _decode_blf2csv(self) -> dict:
        """
        Decode the BLF file and export the data to a CSV file.

        Returns
        -------
        Path
            Directory of the exported CSV files.
        """

        mf4_filename = self._decode_blf2mf4()
        mdf = MDF(mf4_filename)
        csv_file_path = self.output_path / 'csv'
        if not csv_file_path.is_dir():
            csv_file_path.mkdir(parents=True, exist_ok=True)
        mdf.export(filename=csv_file_path, fmt='csv', add_units=False, reduce_memory_usage=True)
        renamer = CSVFileRenamer(self.output_path)
        renamer.rename_files()
        return self._get_data_mapping()

    def _get_data_mapping(self) -> dict:
        """
        Get a mapping of file names to their corresponding paths in the csv directory.

        Parameters:
        ----------
        export_path: Path
            The base path where the 'csv' folder is located.

        Returns: dict
            A dictionary mapping file names to their full paths.
        """
        csv_dir = Path(self.output_path) / 'csv'
        data_mapping: dict = {}

        # Check if the csv directory exists
        if not csv_dir.exists():
            print(f"The directory {csv_dir} does not exist.")
            return data_mapping

        # Iterate over all files in the csv directory
        for file_path in csv_dir.glob('*'):
            if file_path.is_file():
                data_mapping[file_path.stem] = file_path
        return data_mapping

    def decode(self, to_type: str) -> dict | Path:
        """
        Decode the BLF file and export the data to a specified format.

        Parameters
        ----------
        to_type : str
            Output format (mf4 or csv).

        Returns
        -------
        Path
            Output file or directory.
        """
        if to_type == 'mf4':
            return self._decode_blf2mf4()
        elif to_type == 'csv':
            return self._decode_blf2csv()
        else:
            raise ValueError(f"Unsupported output format: {to_type}")
