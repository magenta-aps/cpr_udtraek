# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests

from utility_helpers import get_dk_timestamp

from settings import (
    OIO_API_ENDPOINT,
    OIO_API_RESSOURCE_BRUGER,
    LINIE_ORG_UUID,
    AKTOERREF_UUID
)

# dev
import json


def update_citizen(citizen={}):

    bruger_id = citizen.get('id')

    # NOTE: relationer -> adresser
    adresse_uuid = citizen.get('adresse_uuid')

    # NOTE: relationer -> tilknyttedepersoner
    tilknyt_person = citizen.get('cpr')

    # NOTE: BEGIN - Extracting brugeregenskaber values from citizen dict.

    fornavn = citizen.get('fornavn')
    mellemnavn = citizen.get('mellemnavn')
    efternavn = citizen.get('efternavn')

    brugernavn = fornavn
    if mellemnavn:
        brugernavn += ' {}'.format(mellemnavn)
    brugernavn += ' {}'.format(efternavn)

    civilstand = citizen.get('civilstand')
    koen = citizen.get('koen')

    adressebeskyttelse = citizen.get('adressebeskyttelse')

    current_time = get_dk_timestamp()

    # NOTE: object from database
    bruger_from_db = get_citizen_by_uuid(uuid=bruger_id)

    json_bruger = bruger_from_db.json()

    payload = {}

    attr = json_bruger[bruger_id][0]['registreringer'][0]['attributter']
    attr_virk = attr['brugeregenskaber'][0]['virkning']

    attr['brugeregenskaber'][0]['ava_fornavn'] = fornavn
    attr['brugeregenskaber'][0]['ava_mellemnavn'] = mellemnavn
    attr['brugeregenskaber'][0]['ava_efternavn'] = efternavn
    attr['brugeregenskaber'][0]['brugernavn'] = brugernavn
    attr['brugeregenskaber'][0]['ava_civilstand'] = civilstand
    attr['brugeregenskaber'][0]['ava_koen'] = koen
    attr['brugeregenskaber'][0]['ava_adressebeskyttelse'] = adressebeskyttelse
    attr_virk['from'] = current_time
    attr_virk['to'] = 'infinity'
    payload.update({'attributter': attr})

    rel = json_bruger[bruger_id][0]['registreringer'][0]['relationer']
    payload.update({'relationer': {}})

    addr = rel['adresser']
    addr_virk = addr[0]['virkning']
    addr[0]['uuid'] = adresse_uuid
    addr_virk['from'] = current_time
    addr_virk['to'] = 'infinity'
    addresser = {'adresser': addr}
    payload['relationer'].update(addresser)

    url = '{base_url}/{ressource}/{uuid}'.format(
        base_url=OIO_API_ENDPOINT,
        ressource=OIO_API_RESSOURCE_BRUGER,
        uuid=bruger_id
    )

    response = requests.put(url=url, verify=False, json=payload)

    return response.status_code


def get_citizen_by_uuid(uuid):
    """Get person from LoRa by uuid.
    :type uuid: str
    :returns: Response(requests lib) object
    :rtype: Response"""

    url = '{base_url}/{ressource}/{uuid}'.format(
        base_url=OIO_API_ENDPOINT,
        ressource=OIO_API_RESSOURCE_BRUGER,
        uuid=uuid
    )

    response = requests.get(url, verify=False)

    if response.status_code == 200:

        return response


def get_citizen_uuid_by_cpr(cpr):
    """Get person from LoRa by cpr.
    :type cpr: str
    :returns: Response(requests) object
    :rtype: Response"""

    url = '{base_url}/{ressource}'.format(
        base_url=OIO_API_ENDPOINT,
        ressource=OIO_API_RESSOURCE_BRUGER
    )

    params = {
        'tilknyttedepersoner': 'urn:{cpr}'.format(cpr=cpr)
    }

    response = requests.get(url, verify=False, params=params)

    if response.status_code == 200:

        return response

    else:
        return 'Unexpected response: {}'.format(response.status_code)


def get_all_citizen_uuids():
    """Get citizen references for a given organisation.
    :type org: uuid
    :type org: str
    :returns: List of uuids
    :rtype: list"""

    url = '{base_url}/{ressource}'.format(
        base_url=OIO_API_ENDPOINT,
        ressource=OIO_API_RESSOURCE_BRUGER
    )

    params = {
        'tilhoerer': LINIE_ORG_UUID
    }

    response = requests.get(url, verify=False, params=params)

    if response.status_code == 200:

        response_as_json = json.loads(response.text)

        filtered_result = response_as_json['results'][0]

        return filtered_result

    else:

        return 'Unexpected response: {}'.format(response.status_code)
