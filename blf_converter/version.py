# -*- coding: utf-8 -*-
""" Version declaration of the project """
from pathlib import Path


version = '0.3.0'  # Note: semantic version - major.minor.patch
enable_draft = False

package_name = Path(__file__).parent.name
description = ("The blf_converter tool is designed to facilitate the decoding and conversion of BLF (Binary "
               "Logging Format) files into a readable and analyzable format. This tool is essential for "
               "users who need to interpret and analyze data logged in BLF format. It supports two output "
               "formats and provides functionality for filtering and processing specific signals from the BLF "
               "files.")

repo_url = "https://gitlab.iavgroup.local/cn-tv-a/toolchain/pre_processing/blf_converter.git"

company = "(c) IAV Automotive Engineering (Shanghai) Co., Ltd., 2024, All Rights Reserved."

author = "Qingfeng Yang | Wenbo Guo"
author_email = 'qingfeng.yang@iav.de | wenbo.guo@iav.de'
