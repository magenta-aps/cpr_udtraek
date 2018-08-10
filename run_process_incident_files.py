# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

# NOTE: For development purposes.
from settings import (
    ID_RSA_USER,
    SFTP_SERVER,
    SFTP_SERVER_PORT,
    SFTP_SERVER_INIT_PATH,
    SFTP_DOWNLOAD_PATH,
    ID_RSA_SP_PATH,
    ID_RSA_SP_PASSPHRASE
)

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

settings = {
    'user': ID_RSA_USER,
    'host': SFTP_SERVER,
    'port': SFTP_SERVER_PORT,
    'remote_path': SFTP_SERVER_INIT_PATH,
    'local_path': SFTP_DOWNLOAD_PATH,
    'ssh_key_path': ID_RSA_SP_PATH,
    'ssh_key_passphrase': ID_RSA_SP_PASSPHRASE
}

if __name__ == '__main__':

    start_time = time.monotonic()

    sftpclient = ServiceplatformenSFTPClient(settings)

    sftpclient.open_connection()

    sftpclient.get_incident_files_from_server()

    # NOTE: On remote server move downloaded files to another dir in case
    # something goes wrong, and we therefore would need them.
    # DO NOT STORE IN ./OUT ON SERVER. THE FOLDER IS FOR CPR UDTRAEK DEFINITION FILES !!! 
    sftpclient.move_downloaded_files_on_server()

    sftpclient.close_connection()

    # NOTE: Retrieve an ordered dict( k(datetime), v(path/to/file) ).
    non_processed_files = get_non_processed_files(
        download_dir=SFTP_DOWNLOAD_PATH
    )

    # # NOTE: Parse incident files to dictionaries, and store them in a list.
    incident_dicts = parse_incident_files(
        file_paths_dict=non_processed_files
    )

    for incident_dict in incident_dicts:

        for cpr_no, data in incident_dict.items():

            cit_uuid = get_citizen_uuid_by_cpr(cpr_no)
            content_json = json.loads(cit_uuid.text)

            uuid = content_json.get('results')[0]

            data.update({'id': uuid})

            adresse_uuid = get_address_by_citizen(data)

            data.update({'adresse_uuid': adresse_uuid})

            data.update({'tilknyt_person': cpr_no})

            # update_response = update_citizen(citizen=data)
            #
            # if update_response != 200:
            #     # TODO: Log to root
            #     print(update_response)

    remove_files_from_sftp_download_dir(download_dir=SFTP_DOWNLOAD_PATH)

    end_time = time.monotonic()
    print(timedelta(seconds=end_time - start_time))
