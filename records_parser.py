# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#


def parse_record_001(record):
    """P12170-001 - Personoplysninger.
    Statuskoder:
    01 = Aktiv, bopæl i dansk folkeregister
    03 = Aktiv, speciel vejkode (9900 - 9999) i dansk folkeregister
    05 = Aktiv, bopæl i grønlandsk folkeregister
    07 = Aktiv, speciel vejkode (9900 - 9999) i grønlandsk folkeregister
    20 = Inaktiv, uden bopæl i dansk/grønlandsk folkeregister men tildelt
    personnummer af skattehensyn (kommunekoderne 0010, 0011, 0012 og 0019)
    30 = Inaktiv, anulleret personnummer
    50 = Inaktiv, slettet personnummer ved dobbeltnummer
    60 = Inaktiv, ændret personnummer ved ændring af fødselsdato og køn
    70 = Inaktiv, forsvundet
    80 = Inaktiv, udrejst
    90 = Inaktiv, død

    :param record: Time of incident file' creation
    :type record: str
    :return: Nested dictionary -> { cprnr: { k:v, k:v, .. } }
    :rtype: dict"""

    record_dict = {}
    record_dict['RECORDTYPE'] = record[0:3].strip()
    record_dict['PNR'] = record[3:13].strip()
    record_dict['PNRGAELD'] = record[13:23].strip()
    record_dict['STATUS'] = record[23:25].strip()
    record_dict['STATUSHAENSTART'] = record[25:37].strip()
    record_dict['STATUSDTO_UMRK'] = record[37:38].strip()
    record_dict['KOEN'] = record[38:39].strip()
    record_dict['FOED_DT'] = record[39:49].strip()
    record_dict['FOED_DT_UMRK'] = record[49:50].strip()
    record_dict['START_DT-PERSON'] = record[50:60].strip()
    record_dict['START_DT_UMRK-PERSON'] = record[60:61].strip()
    record_dict['SLUT_DT-PERSON'] = record[61:71].strip()
    record_dict['SLUT_DT_UMRK-PERSON'] = record[71:72].strip()
    record_dict['STILLING'] = record[72:106].strip()
    return record_dict


def parse_record_003(record):
    """P12170-002 - Aktuelle adresseoplysninger.
    For personer hvor status > eller = 30, vil det kun være feltet adrnvn
    der er udfyldt. Se statusbrskrivelser i docstring for parse_record_001()"""

    record_dict = {}
    record_dict['RECORDTYPE'] = record[0:3].strip()
    record_dict['PNR'] = record[3:13].strip()
    record_dict['ADRNVN'] = record[13:47].strip()
    record_dict['CONVN'] = record[47:81].strip()
    record_dict['LOKALITET'] = record[81:115].strip()
    record_dict['STANDARDADR'] = record[115:149].strip()
    record_dict['BYNVN'] = record[149:183].strip()
    record_dict['POSTNR'] = record[183:187].strip()
    record_dict['POSTDISTTXT'] = record[187:207].strip()
    record_dict['KOMKOD'] = record[207:211].strip()
    record_dict['VEJKOD'] = record[211:215].strip()
    record_dict['HUSNR'] = record[215:219].strip()
    record_dict['ETAGE'] = record[219:221].strip()
    record_dict['SIDEDOER'] = record[221:225].strip()
    record_dict['BNR'] = record[225:229].strip()
    record_dict['VEJADRNVN'] = record[229:249].strip()
    return record_dict


def parse_record_004(record):
    """P12170-004 - Beskyttelse.
    0001 = Navne- og adressebeskyttelse
    0002 = Lokalvejviserbeskyttelse
    0003 = Markedsføringsbeskyttelse"""

    record_dict = {}
    record_dict['RECORDTYPE'] = record[0:3].strip()
    record_dict['PNR'] = record[3:13].strip()
    record_dict['BESKYTTYPE'] = record[13:17].strip()
    record_dict['START_DT-BESKYTTELSE'] = record[17:27].strip()
    record_dict['SLET_DT-BESKYTTELSE'] = record[27:37].strip()
    return record_dict


def parse_record_008(record):
    """P12170-008 - Aktuelle navneoplysinger.
    # FORNVN_MRK, MELNVN_MRK og EFTERNVN_MRK
    # + = Navnet er forkortet.
    # * = Navnet indeholder tegn der ikke kan indrapporteres til CPR.
    # = = Navnet er utilstrækkeligt dokumenteret."""

    record_dict = {}
    record_dict["RECORDTYPE"] = record[0:3].strip()
    record_dict["PNR"] = record[3:13].strip()
    record_dict["FORNVN"] = record[13:63].strip()
    record_dict["FORNVN_MRK"] = record[63:64].strip()
    record_dict["MELNVN"] = record[64:104].strip()
    record_dict["MELNVN_MRK"] = record[104:105].strip()
    record_dict["EFTERNVN"] = record[105:145].strip()
    record_dict["EFTERNVN_MRK"] = record[145:146].strip()
    record_dict["NVNHAENSTART"] = record[146:158].strip()
    record_dict["HAENSTART_UMRK-NAVNE"] = record[158:159].strip()
    record_dict["ADRNVN"] = record[159:193].strip()
    return record_dict


def parse_record_012(record):
    """P12170-012 - Aktuel civilstand.
    Civilstand - CIVST
    U = Ugift
    G = Gift
    F = Fraskilt
    E = Enke/enkemand
    P = Registreret partnerskab
    O = Ophævet partnerskab
    L = Længestlevende partner
    D = Død
    ---------------
    Hvis ægtefælle har et personnummer vil AEGTEPNR være udfyldt,og felterne
    ægtefælle fødselsdato (AEGTEFOED_DT) og ægtefælle navn (AEGTENVN) blankt"""

    record_dict = {}
    record_dict["RECORDTYPE"] = record[0: 3].strip()
    record_dict["PNR"] = record[3: 13].strip()
    record_dict["CIVST"] = record[13: 14].strip()
    record_dict["AEGTEPNR"] = record[14: 24].strip()
    record_dict["AEGTEFOED_DT"] = record[24: 34].strip()
    record_dict["AEGTEFOEDDT_UMRK"] = record[35: 35].strip()
    record_dict["AEGTENVN"] = record[35: 69].strip()
    record_dict["AEGTENVN_MRK"] = record[69: 70].strip()
    record_dict["HAENSTART-CIVILSTAND"] = record[70: 82].strip()
    record_dict["HAENSTART_UMRK-CIVILSTAND"] = record[82: 83].strip()
    record_dict["SEP_HENVIS-CIVILSTAND"] = record[83: 95].strip()
    return record_dict
