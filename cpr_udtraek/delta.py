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
import logging
import os
from cpr_udtraek.sftp_client import ServiceplatformenSFTPClient
from cpr_udtraek.file_parser import parse_incident_files

logger = logging.getLogger("cpr_udtraek")

settings = {
    'user': ID_RSA_USER,
    'host': SFTP_SERVER,
    'port': SFTP_SERVER_PORT,
    'remote_path': SFTP_SERVER_INIT_PATH,
    'local_path': SFTP_DOWNLOAD_PATH,
    'ssh_key_path': ID_RSA_SP_PATH,
    'ssh_key_passphrase': ID_RSA_SP_PASSPHRASE
}

def delta(since_ymd="010101"):
    logger.info("start cpr_udtraek delta siden %(since_ymd)s", locals())
    sftpclient = ServiceplatformenSFTPClient(settings)
    sftpclient.open_connection()
    files = sftpclient.get_files(since_ymd=since_ymd)
    sftpclient.close_connection()
    citizen_changes_by_date = parse_incident_files(files)
    filelist = [f for f in os.listdir(SFTP_DOWNLOAD_PATH)]
    for f in filelist:
        os.remove(os.path.join(SFTP_DOWNLOAD_PATH, f))
    logger.info("end cpr_udtraek delta siden %(since_ymd)s", locals())
    return citizen_changes_by_date


