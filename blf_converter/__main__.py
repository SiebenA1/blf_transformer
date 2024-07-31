# -*- coding: utf-8 -*-
"""Main script of current project"""
from blf_converter.common.blf_converter import BlfConverter
from blf_converter.module.args_parser import parser


def main():
    args = parser.parse_args()
    args_dict = vars(args)
    blf = args_dict.get("blf_file")
    dbc = args_dict.get("dbc_file")
    signal_list = args_dict.get("signal_list")
    blf_converter = BlfConverter(blf, dbc, signal_list)
    blf_converter.decode(to_type='csv')


if __name__ == '__main__':
    main()
