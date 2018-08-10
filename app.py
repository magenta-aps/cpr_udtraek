# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import sys
import json
import time
from datetime import timedelta
from dawa_client import get_address_by_citizen
from file_helpers import get_non_processed_files
from sftp_client import ServiceplatformenSFTPClient
from file_parser import parse_incident_files
from file_helpers import remove_files_from_sftp_download_dir
from oio_client import (
    get_citizen_uuid_by_cpr,
    update_citizen
)


def run_application(settings={}):

    sftpclient = ServiceplatformenSFTPClient(settings)
    sftpclient.open_connection()
    sftpclient.get_incident_files_from_server()
    sftpclient.move_downloaded_files_on_server()
    sftpclient.close_connection()

    non_processed_files = get_non_processed_files(
        download_dir=SFTP_DOWNLOAD_PATH
    )

    incident_dicts = parse_incident_files(
        file_paths_dict=non_processed_files
    )

    # for incident_dict in incident_dicts:
    #
    #     for cpr_no, data in incident_dict.items():
    #
    #         cit_uuid = get_citizen_uuid_by_cpr(cpr_no)
    #         content_json = json.loads(cit_uuid.text)
    #         uuid = content_json.get('results')[0]
    #         data.update({'id': uuid})
    #         adresse_uuid = get_address_by_citizen(data)
    #         data.update({'adresse_uuid': adresse_uuid})
    #         data.update({'tilknyt_person': cpr_no})
    #
    #         update_response = update_citizen(citizen=data)
    #
    #         if update_response != 200:
    #             # TODO: Log to root
    #             print(update_response)

    remove_files_from_sftp_download_dir(download_dir=SFTP_DOWNLOAD_PATH)
