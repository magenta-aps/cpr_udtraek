# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import paramiko
import errno
import os


class ServiceplatformenSFTPClient(object):

    def __init__(self, settings={}):
        """Constructor.
        :param settings: user, host, port, remote_path, local_path, ssh_key,
        ssh_key_passphrase
        :type settings: dict
        :return: void
        :rtype: None"""

        self.username = settings.get('user')
        self.host = settings.get('host')
        self.port = int(settings.get('port', 22))
        self.remote_path = settings.get('remote_path')
        self.localpath = settings.get('local_path')

        if not os.path.isdir(self.localpath):
            raise NotADirectoryError(self.localpath)

        self.key = paramiko.RSAKey.from_private_key_file(
            filename=settings.get('ssh_key_path'),
            password=settings.get('ssh_key_passphrase')
        )

        self.transport = paramiko.Transport((self.host, self.port))
        self.downloaded_files = []

    def open_connection(self):
        """Opens connection to sftp server.
        :return: void
        :rtype: None"""

        self.transport.connect(username=self.username, pkey=self.key)
        self.sftp_client = paramiko.SFTPClient.from_transport(self.transport)

    def close_connection(self):
        """Closes connection to sftp server.
        :return: void
        :rtype: None"""

        self.sftp_client.close()
        self.transport.close()

    def get_files(self, since_ymd):
        """Downloads all current incident files on serviceplatformen' sftp
        server, and stores them in locally defined local file storage path.
        :return: A list of the files downloaded.
        :rtype: list"""

        remote_to_local = [
            (os.path.join(self.remote_path, filename), os.path.join(self.localpath, filename))
            for filename in self.sftp_client.listdir(self.remote_path) 
            if filename[1:] > since_ymd
            and not filename.endswith(".metadata")
        ]

        for remote, local in remote_to_local:
            self.sftp_client.get(remote, local)

        return [local for remote,local in remote_to_local]

