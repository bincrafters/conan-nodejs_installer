#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanException


class NodejsInstallerConan(ConanFile):
    name = "nodejs_installer"
    version = "10.15.0"
    description = "nodejs binaries for use in recipes"
    topics = ("conan", "node", "nodejs")
    url = "https://github.com/bincrafters/conan-nodejs_installer"
    homepage = "https://nodejs.org"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = "nodejs.patch"
    settings = "os_build", "arch_build"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _autotools = None

    def source(self):
        if self.settings.os_build == "Linux" and self.settings.arch_build == "x86":
            tools.get("https://nodejs.org/dist/v10.15.0/node-v10.15.0.tar.gz")
            os.rename("node-v10.15.0", self._source_subfolder)
        else:
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
                raise ConanException("actual os is not supported")

            filename = "node-v{}-{}-{}".format(self.version, platform, arch)
            source_url = "{}/dist/v{}/{}.{}".format(self.homepage, self.version, filename, extension)
            tools.get(source_url)
            extracted_dir = filename
            os.rename(extracted_dir, self._build_subfolder)


    # def build_requirements(self):
    #     if self.settings.os_build == "Linux" and self.settings.arch_build == "x86":
    #         self.build_requires("OpenSSL/1.0.2o@conan/stable")

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self)
            # args = ['--fully-static',
            #         '--shared-openssl',
            #         ('--shared-openssl-includes=%s' % self.deps_cpp_info["OpenSSL"].include_paths[0]),
            #         ('--shared-openssl-libpath=%s' % self.deps_cpp_info["OpenSSL"].lib_paths[0])
            #     ]
            self._autotools.configure()
        return self._autotools

    def build(self):
        if self.settings.os_build == "Linux" and self.settings.arch_build == "x86":
            # tools.patch(base_path=self._source_subfolder, patch_file="nodejs.patch")
            print("PWD: %s" % os.getcwd())
            with tools.chdir(self._source_subfolder):
                autotools = self._configure_autotools()
                env_build_vars = autotools.vars
                env_build_vars['PARALLEL_ARGS'] = '--flaky-tests=skip'
                autotools.make(vars=env_build_vars)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._build_subfolder)
        if self.settings.os_build == "Linux" and self.settings.arch_build == "x86":
            with tools.chdir(self._source_subfolder):
                autotools = self._configure_autotools()
                autotools.install()
                for package_subfolder in ["include", "lib", "share"]:
                    shutil.rmtree(os.path.join(self.package_folder, package_subfolder))
        else:
            self.copy(pattern="*", src=self._build_subfolder, dst="", keep_path=True)

    def package_info(self):
        bin_dir = self.package_folder if tools.os_info.is_windows else os.path.join(self.package_folder, "bin")
        self.env_info.PATH.append(bin_dir)
