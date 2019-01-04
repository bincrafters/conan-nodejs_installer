#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, tools
import os


class TestPackageConan(ConanFile):

    def test(self):
        self.run("node --version")
