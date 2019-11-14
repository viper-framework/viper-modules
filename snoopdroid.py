# -*- coding: utf-8 -*-
# This file is part of Viper - https://github.com/viper-framework/viper
# See the file 'LICENSE' for copying permission.

from viper.common.abstracts import Module
from viper.core.project import __project__

try:
    import snoopdroid
    HAVE_SNOOPDROID = True
except ImportError:
    HAVE_SNOOPDROID = False

class Snoopdroid(Module):
    cmd = "snoopdroid"
    description = "Download applications from Android phone"
    authors = ["nex"]
    categories = ["android"]

    def __init__(self):
        super(Snoopdroid, self).__init__()
        self.parser.add_argument("-l", "--list", action="store_true", help="Get a list of packages installed")
        self.parser.add_argument("-p", "--packages", action="store", help="Download only specific package names (comma separated)")
        self.parser.add_argument("-a", "--all", action="store_true", help="Download all installed applications from Android phone (and store in open project)")

    def _get_packages(self):
        acq = snoopdroid.Acquisition(all_apks=True)
        acq.connect()
        acq.get_packages()
        acq.disconnect()
        for package in acq.packages:
            self.log("item", package.name)

    def _download_all(self):
        project_path = __project__.get_path()

        acq = snoopdroid.Acquisition(storage_folder="/tmp", all_apks=True)
        acq.connect()
        acq.get_packages()
        acq.pull_packages()
        acq.disconnect()

    def run(self):
        super(Snoopdroid, self).run()
        if self.args is None:
            return

        if not HAVE_SNOOPDROID:
            self.log("error", "Missing dependency, install snoopdroid (`pip3 install snoopdroid`)")
            return

        if self.args.list:
            self._get_packages()
        elif self.args.all:
            self._download_all()
        elif self.args.packages:
            # TODO
            self.log("warning", "Not implemented yet")
