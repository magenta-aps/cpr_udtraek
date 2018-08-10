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
import requests


def get_address_by_citizen(citizen_data):
    """Description pending..."""

    url = 'https://dawa.aws.dk/adresser'

    # Strip leading 0 (zeros)
    etage = citizen_data.get('etage')
    husnummer = citizen_data.get('husnr')
    postnummer = citizen_data.get('postnr')
    sidedoer = citizen_data.get('sidedoer')
    vejkode = citizen_data.get('vejkode')

    # NOTE: If one of these is empty we have flawed address data.
    if husnummer is '' or postnummer is '' or vejkode is '':
        return False

    husnummer = husnummer.lstrip('0')

    params = {
        'vejkode': vejkode,
        'husnr': husnummer,
        'postnr': postnummer,
        'struktur': 'mini'
    }

    if etage:
        etage = etage.lstrip('0')
        params.update({'etage': etage})

    if sidedoer:
        sidedoer = sidedoer.lstrip('0')
        params.update({'dør': sidedoer})

    response = requests.get(url, params=params)

    try:

        response_dict = response.json()[0].get('id')
        return response_dict

    except Exception as e:

        error_dict = {
            'exception': e,
            'file': __file__,
            'function': sys._getframe(0).f_code.co_name,
            'function input parameter': citizen_data,
            'http request parameters': params
        }
        return error_dict
