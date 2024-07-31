# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

import pandas as pd


class CSVFileRenamer:
    """
    A class to rename CSV files based on it's second column name.
    """

    def __init__(self, export_path: Path):
        self.export_path = export_path

    @staticmethod
    def _get_signal_name(csv_file_path: Path) -> str | bool:
        """
        Get the name of the signal from the second column of the CSV file.


        Returns
        -------
        str
            The name of the signal.
        """
        try:
            df = pd.read_csv(csv_file_path, nrows=0)
            column_names = df.columns
            if len(column_names) > 1:
                name = column_names[1]
                return name
            else:
                raise ValueError(f"The file {csv_file_path} does not have a second column.")
        except Exception as e:
            print(f"Error reading {csv_file_path}: {e}")
            return False

    def rename_files(self) -> bool:
        """
        Rename the CSV files based on the second column name.

        Returns
        -------
        bool
            True if the file is renamed successfully, False otherwise.
        """
        status = True
        for file_path in self.export_path.glob('*.csv'):
            new_file_name = self._get_signal_name(file_path)
            if new_file_name:
                new_file_path = self.export_path.joinpath('csv', f"{new_file_name}.csv")
                if not new_file_path.exists():
                    shutil.move(file_path, new_file_path)
                    status = True
                else:
                    print(f"Cannot rename '{file_path.name}' to '{new_file_name}.csv' as the file already exists.")
                    status = False
            else:
                print(f"Skipping file '{file_path.name}' due to error in reading the second column name.")
                status = False
        return status
