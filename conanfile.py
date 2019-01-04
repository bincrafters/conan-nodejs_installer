#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class NodejsInstallerConan(ConanFile):
    name = "nodejs_installer"
    version = "10.15.0"
    description = "nodejs binaries for use in recipies"
    topics = ("conan", "node", "nodejs", "logging")
    url = "https://github.com/bincrafters/conan-nodejs_installer"
    homepage = "https://nodejs.org"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    settings = "os_build", "arch_build"
    short_paths = True

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "{}-{}".format(name, version)
    _build_subfolder = _source_subfolder

    def build(self):
        arch = "x64" if self.settings.arch_build == "x86_64" else "x86"
        if tools.os_info.is_windows:
            platform = "win"
            extension = "zip"
        elif tools.os_info.is_macos:
            platform = "darwin"
            extension = "tar.gz"
        elif tools.os_info.is_linux:
            platform = "linux"
            extension = "tar.xz"
        else:
            raise Exception("actual os is not supported")

        filename = "node-v{}-{}-{}".format(self.version, platform, arch)
        source_url = "https://nodejs.org/dist/v{}/{}.{}".format(self.version, filename, extension)
        self.output.info("Download {}".format(source_url))
        tools.get(source_url)
        extracted_dir = filename
        os.rename(extracted_dir, self._build_subfolder)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._build_subfolder)
        self.copy(pattern="*", src=self._build_subfolder, dst="", keep_path=True)

    def package_info(self):
        bin_dir = os.path.join(self.package_folder, "bin")
        if tools.os_info.is_windows:
            bin_dir = self.package_folder
        self.env_info.PATH.append(bin_dir)
