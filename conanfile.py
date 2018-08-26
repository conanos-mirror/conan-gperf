
import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment


class GperfConan(ConanFile):
    name = "gperf"
    version = "3.1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gperf here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        url = 'http://ftp.gnu.org/pub/gnu/gperf/gperf-{version}.tar.gz'
        tools.get(url.format(version=self.version))

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir="{name}-{version}".format(name=self.name, version=self.version))
        autotools.make()

    def package(self):
        with tools.chdir(self.build_folder):
            self.run("make install")

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))

