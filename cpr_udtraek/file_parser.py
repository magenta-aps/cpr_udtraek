# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

from .records_parser import (
    parse_record_001,
    parse_record_003,
    parse_record_004,
    parse_record_008,
    parse_record_012
)

import json
import sys
import os
import datetime
import logging

logger = logging.getLogger("cpr_udtraek")

def parse_incident_files(files):
    """Description pending...
    :param file_path: Location of incident file(s)
    :type file_path: str
    :return: A list containing dictionaries parsed from incident files.
    :rtype: list"""

    citizen_changes_by_date = {}
    for file_path in sorted(files):
        # changes for a citizen is aggregated by date
        date = os.path.basename(file_path)[1:7]
        citizen_changes = citizen_changes_by_date.setdefault(date,{})
        __parse_incident_file(citizen_changes, file_path=file_path)
    return citizen_changes_by_date


def __parse_incident_file(citizens, file_path):
    """Description pending...
    :param date: Time of incident file' creation
    :param file_path: Location of incident file
    :type date: str
    :type file_path: str
    :return: Nested dictionary -> { cprnr: { k:v, k:v, .. } }
    :rtype: dict"""

    logger.info("parsing %(file_path)s", locals())

    try:
        cpr_file_fp = open(file_path, 'r', encoding='ISO-8859-1')

        for line in cpr_file_fp:

            # NOTE: Ignoring non-citizen records: 000, 910, 997, 999
            if (line[0:3] == '000' or
                    line[0:3] == '910' or
                    line[0:3] == '997' or
                    line[0:3] == '999'):

                # Do nothing
                pass

            else:

                cprnr = line[3:13]

                # NOTE: If cprnr is not a key in dict we add it.
                if cprnr not in citizens:
                    citizens[cprnr] = {}

                # NOTE: Extracting gender.
                if line[0:3] == '001':
                    record_001_dict = parse_record_001(record=line)
                    koen = record_001_dict['KOEN']
                    citizens[cprnr].update({'koen': koen})

                # NOTE: Extracting address.
                if line[0:3] == '003':
                    record_003_dict = parse_record_003(record=line)

                    # Extract values record_003_dict.
                    vejkode = record_003_dict['VEJKOD']
                    husnr = record_003_dict['HUSNR']
                    etage = record_003_dict['ETAGE']
                    sidedoer = record_003_dict['SIDEDOER']
                    postdistrikt = record_003_dict['POSTDISTTXT']
                    postnr = record_003_dict['POSTNR']
                    kommunekode = record_003_dict['KOMKOD']

                    # Insert extracted values into citizens dict.
                    citizens[cprnr].update({'vejkode': vejkode})
                    citizens[cprnr].update({'husnr': husnr})
                    citizens[cprnr].update({'etage': etage})
                    citizens[cprnr].update({'sidedoer': sidedoer})
                    citizens[cprnr].update({'postdistrikt': postdistrikt})
                    citizens[cprnr].update({'postnr': postnr})
                    citizens[cprnr].update({'kommunekode': kommunekode})

                # NOTE: Extracting privacy information.
                if line[0:3] == '004':
                    record_004_dict = parse_record_004(record=line)
                    beskyttelsestype = record_004_dict['BESKYTTYPE']
                    beskyttelse_start = record_004_dict['START_DT-BESKYTTELSE']
                    beskyttelse_stop = record_004_dict['SLET_DT-BESKYTTELSE']
                    if beskyttelsestype == '0001':
                        citizens[cprnr].update({
                            'adressebeskyttelse': True,
                            'adressebeskyttelse_start': beskyttelse_start,
                            'adressebeskyttelse_stop': beskyttelse_stop
                        })

                # NOTE: Extracting name.
                if line[0:3] == '008':
                    record_008_dict = parse_record_008(record=line)
                    fornavn = record_008_dict['FORNVN']
                    mellemnavn = record_008_dict['MELNVN']
                    efternavn = record_008_dict['EFTERNVN']
                    citizens[cprnr].update({'fornavn': fornavn})
                    citizens[cprnr].update({'mellemnavn': mellemnavn})
                    citizens[cprnr].update({'efternavn': efternavn})

                # NOTE: Extracting marital status.
                if line[0:3] == '012':
                    record_012_dict = parse_record_012(record=line)
                    civilstand = record_012_dict['CIVST']
                    citizens[cprnr].update({'civilstand': civilstand})

    except Exception as e:

        logger.exception(e)
