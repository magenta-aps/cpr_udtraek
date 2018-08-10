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

        try:
            os.makedirs(self.localpath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print(e)
                raise

        try:
            self.key = paramiko.RSAKey.from_private_key_file(
                filename=settings.get('ssh_key_path'),
                password=settings.get('ssh_key_passphrase')
            )
        except IOError as e:
            print(e)

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

    def get_incident_files_from_server(self):
        """Downloads all current incident files on serviceplatformen' sftp
        server, and stores them in locally defined local file storage path.
        :return: A list of the files downloaded.
        :rtype: list"""

        filenames = self.sftp_client.listdir(self.remote_path)

        for filename in filenames:

            remote_file_path = '{}{}'.format(self.remote_path, str(filename))
            local_file_path = '{}/{}'.format(self.localpath, str(filename))
            self.downloaded_files.append(remote_file_path)
            self.sftp_client.get(remote_file_path, local_file_path)

        return filenames

    def move_downloaded_files_on_server(self):
        """Uses the instance variable downloaded_files[] as reference to
        respectively move processed files from /IN/ to /OUT/ on the
        sftp server. The file references in self.downloaded_files are appended
        during execution of get_incident_files_from_server().
        :param downloaded_files: A list of file names.
        :type downloaded_files: list
        :return: void
        :rtype: None"""

        remote_files = self.downloaded_files
        for current_filepath in remote_files:
            filename = current_filepath[5:]
            new_filepath = '/{target_dir}/{filename}'.format(
                target_dir='OUT',
                filename=filename
            )
            # print(new_filepath)
            self.sftp_client.rename(current_filepath, new_filepath)
