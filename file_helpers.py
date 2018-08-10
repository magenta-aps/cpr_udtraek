# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os
import collections


def get_non_processed_files(download_dir):
    """Walks sftp file directory. If files are empty they are deleted,
    if not then are added to a dictionary, and sorted based on date.
    :return: Nested dictionary order by key(date) -> { date: file_path, .. }
    :rtype: dict"""

    file_path_dict = {}

    for dir_name, sub_dir_list, file_list in os.walk(download_dir):

        for file_name in file_list:

            if not(file_name.endswith(".metadata")):

                file_path = '{}/{}'.format(download_dir, file_name)

                file_empty = is_file_empty(file_path)

                if file_empty:

                    remove_file_from_sftp_download_dir(file_path)

                else:

                    file_path_dict[file_name[1:7]] = '{}/{}'.format(
                        dir_name,
                        file_name
                    )

    file_path_dict = collections.OrderedDict(
        sorted(file_path_dict.items())
    )

    if bool(file_path_dict):
        return file_path_dict
    else:
        return {'Warning': 'No files in specified sftp download directory.'}


def is_file_empty(file_path):
    """Checks whether the file contains citizen records, or not.
    :param file_path: Location of incident file
    :type file_path: str
    :return: Boolean
    :rtype: bool"""

    try:

        cpr_file = open(file_path, 'r', encoding='ISO-8859-1')

        # NOTE: Index '1' is the second line the file. If the line contains a
        # record type '999' then we know we hit the end of the the file.
        record_type = cpr_file.readlines()[1][:3]

        if record_type == '999':
            return True
        else:
            return False

    except Exception as e:
        print(e)


def remove_files_from_sftp_download_dir(download_dir):
    """Removes referenced incident- and respective metadata file.
    :param file_path: Location of incident file
    :type file_path: str
    :return: Void
    :rtype: None"""

    filelist = [f for f in os.listdir(download_dir)]
    for f in filelist:
        os.remove(os.path.join(download_dir, f))
