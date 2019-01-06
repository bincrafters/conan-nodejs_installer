#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
from conans.client import conan_api


if __name__ == "__main__":
    print("CONAN ENTRYPOINT: START!")
    instance, _, _ = conan_api.Conan.factory()
    instance.export(path=".", name="nodejs_installer", version="10.15.0", user=os.getenv("CONAN_USERNAME", "bincrafters"), channel=os.getenv("CONAN_CHANNEL", "stable"))
    instance.install(path=".", install_folder="/tmp/install")
    instance.source(path=".", source_folder="/tmp/source", info_folder="/tmp/install")
    shutil.copytree("/tmp/source", "/tmp/build")
    instance.build(conanfile_path=".", source_folder="/tmp/source", package_folder="/tmp/package", install_folder="/tmp/install", build_folder="/tmp/build")
    instance.package(path=".", source_folder="/tmp/source", package_folder="/tmp/package", build_folder="/tmp/build", install_folder="/tmp/install")
    print("CONAN ENTRYPOINT: END!")