# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from datetime import datetime
import datetime as dt
import pytz
import re


def get_dk_timestamp():
    """Returns String timestamp -> Y-m-d H:M:S z"""
    local_tz = pytz.timezone("Europe/Copenhagen")
    dtz = dt.datetime.now(tz=pytz.UTC)
    local_dtz = dtz.replace(tzinfo=pytz.utc).astimezone(local_tz)
    string_format = local_dtz.strftime("%Y-%m-%d %H:%M:%S %z")
    dk_timestamp = string_format[0:19] + string_format[20:23]
    return dk_timestamp


def validate_cpr(cpr):
    if cpr:
        check = re.match(r'^\d{10}$', cpr)
        if check:
            return True
        else:
            return False
    else:
        return False


def validate_uuid(uuid):
    if uuid:
        expr = (r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}'
                '-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}')
        check = re.match(expr, uuid)
        if check:
            return True
        else:
            return False
    else:
        return False
