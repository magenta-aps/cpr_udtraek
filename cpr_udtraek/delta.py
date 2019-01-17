# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import sys
import logging
import os
from cpr_udtraek.sftp_client import ServiceplatformenSFTPClient
from cpr_udtraek.file_parser import parse_incident_files


logger = logging.getLogger("cpr_udtraek")


def delta(since_ymd="010101", settings={}):
    logger.info("start cpr_udtraek delta siden %(since_ymd)s", locals())
    sftpclient = ServiceplatformenSFTPClient(settings)
    sftpclient.open_connection()
    files = sftpclient.get_files(since_ymd=since_ymd)
    sftpclient.close_connection()
    citizen_changes_by_date = parse_incident_files(files)
    filelist = [f for f in os.listdir(settings["local_path"])]
    for f in filelist:
        os.remove(os.path.join(settings["local_path"], f))
    logger.info("end cpr_udtraek delta siden %(since_ymd)s", locals())
    return citizen_changes_by_date

if __name__ == '__main__':
    testit = False
    if testit:
        print(delta())
