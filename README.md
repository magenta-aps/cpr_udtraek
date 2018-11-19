# cpr_udtraek


a program could look like this

    settings = {
        'user': ID_RSA_USER,
        'host': SFTP_SERVER, 
        'port': SFTP_SERVER_PORT,
        'remote_path': SFTP_SERVER_INIT_PATH,
        'local_path': SFTP_DOWNLOAD_PATH,
        'ssh_key_path': ID_RSA_SP_PATH,
        'ssh_key_passphrase': ID_RSA_SP_PASSPHRASE
    }

    from cpr_udtraek import delta
    import pprint

    import logging
    logging.basicConfig(level=logging.INFO)

    citizen_changes_by_date = delta("180927", settings=settings)

    changedate = list(citizen_changes_by_date.keys())[0]
    print (changedate)

    changes_for_the_day = citizen_changes_by_date[changedate]
    some_cpr_number = list(changes_for_the_day.keys())[0]
    print(some_cpr_number)

    changes_for_some_cpr_number_on_changedate = changes_for_the_day[some_cpr_number]
    pprint.pprint(changes_for_some_cpr_number_on_changedate)

It could give log and output like this

    INFO:cpr_udtraek:start cpr_udtraek delta siden 180927
    INFO:paramiko.transport:Connected (version 2.0, client OpenSSH_7.2p2)
    INFO:paramiko.transport:Authentication (publickey) successful!
    INFO:paramiko.transport.sftp:[chan 0] Opened sftp connection (server version 3)
    INFO:paramiko.transport.sftp:[chan 0] sftp session closed.
    INFO:cpr_udtraek:parsing /cpr-files/D180927.L123456
    INFO:cpr_udtraek:end cpr_udtraek delta siden 180927
    180928
    0101961234
    {'civilstand': 'E',
     'efternavn': 'Udzen',
     'etage': '',
     'fornavn': 'Ane Ulrike',
     'husnr': '016',
     'koen': 'K',
     'kommunekode': '0851',
     'mellemnavn': '',
     'postdistrikt': 'Aalborg',
     'postnr': '9000',
     'sidedoer': '',
     'vejkode': '8511'}

Where 

* 180928 is the date the changes are effective
* 0101961234 is the person number of the person 
* {...} is the changes for the person, in this case a changed address


